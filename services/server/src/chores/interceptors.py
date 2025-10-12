from collections.abc import Callable

from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException
from jose import jwt as jose_jwt
from jwt import PyJWKClient
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError, InvalidTokenError

from chores.config import Config
from chores.deps import Container
from chores.errors import Unauthenticated


class ExceptionToStatusInterceptor(ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request_or_iterator,
        context: _Context,
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
        context: _Context,
        method_name: str,
        config: Config = Provide[Container.config],
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

        return method(request_or_iterator, context)
