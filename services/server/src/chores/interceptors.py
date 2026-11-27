from collections.abc import Callable

from dependency_injector.wiring import inject, Provide
from grpc import ServicerContext
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException
from jose import jwt as jose_jwt
from jwt import PyJWKClient
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError, InvalidTokenError

from chores.auth import current_caller, current_user_email, current_user_sub, require_caller
from chores.config import Config
from chores.db import Database
from chores.deps import Container
from chores.errors import Unauthenticated

# First login creates the user, so this RPC has no caller row yet.
_SKIP_CALLER_LOOKUP = {"/chores.Users/SyncUser"}


class ExceptionToStatusInterceptor(ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request_or_iterator,
        context: ServicerContext,
        method_name: str,
    ):
        try:
            return method(request_or_iterator, context)
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise e


class AuthInterceptor(ServerInterceptor):
    @inject
    def intercept(
        self,
        method: Callable,
        request_or_iterator,
        context: ServicerContext,
        method_name: str,
        config: Config = Provide[Container.config],
        database: Database = Provide[Container.database],
    ):
        if method_name == "/chores.Users/Login" or method_name == "/chores.Users/Register":
            return method(request_or_iterator, context)

        metadata = context.invocation_metadata()
        if metadata is None or len(metadata) == 0:
            raise Unauthenticated("Missing token")

        try:
            token_metadata = next(datum for datum in metadata if datum.key.lower() == "authorization")
            token = token_metadata.value.removeprefix("Bearer").strip()
            public_key_url = f"https://{config.auth0.domain}/.well-known/jwks.json"
            jwks_client = PyJWKClient(public_key_url, cache_keys=True)
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            decoded_token = jose_jwt.decode(
                token, signing_key.key, algorithms=["RS256"], audience=config.auth0.audience
            )
            assert decoded_token["iss"].removeprefix("https://").removesuffix("/").strip() == config.auth0.domain
            sub = decoded_token["sub"]

        except ExpiredSignatureError:
            raise Unauthenticated("Token has expired")
        except (InvalidTokenError, InvalidAudienceError, KeyError):
            raise Unauthenticated("Invalid token")
        except StopIteration:
            raise Unauthenticated("Missing token")
        except AssertionError:
            raise Unauthenticated("Invalid token issuer")
        except Exception as e:
            raise Unauthenticated(f"Authentication failed: {e!s}")

        if not isinstance(sub, str) or not sub.strip():
            raise Unauthenticated("Invalid token subject")

        email = decoded_token.get("email")
        token_email = email.strip() if isinstance(email, str) and email.strip() else None
        sub_token = current_user_sub.set(sub)
        email_token = current_user_email.set(token_email)
        caller_token = None
        try:
            if method_name not in _SKIP_CALLER_LOOKUP:
                with database.session() as db:
                    caller = require_caller(db)
                    db.expunge(caller)
                caller_token = current_caller.set(caller)
            return method(request_or_iterator, context)
        finally:
            if caller_token is not None:
                current_caller.reset(caller_token)
            current_user_sub.reset(sub_token)
            current_user_email.reset(email_token)
