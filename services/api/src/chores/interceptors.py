from collections.abc import Callable

import jwt
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from chores.config import Config
from chores.deps import Container
from chores.errors import Unauthenticated

UNAUTHENTICATED_ROUTES = [
    "/chores.Users/Login",
    "/chores.Users/Register",
    "/chores.Users/ValidateRegisterPayload",
    "/chores.Users/ValidateLoginPayload",
]


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
        if method_name in UNAUTHENTICATED_ROUTES:
            return method(request_or_iterator, context)

        metadata = context.invocation_metadata()
        if metadata is None or len(metadata) == 0:
            raise Unauthenticated("Missing token")

        try:
            token_metadata = next(datum for datum in metadata if datum.key.lower() == "authorization")
            token = token_metadata.value.removeprefix("Bearer ")
            jwt.decode(
                token, config.cryptography.secret_key, algorithms=["HS256"]
            )  # Replace with a better algo, check for expiration
        except ExpiredSignatureError:
            raise Unauthenticated("Token has expired")
        except InvalidTokenError:
            raise Unauthenticated("Invalid token")
        except StopIteration:
            raise Unauthenticated("Missing token")

        return method(request_or_iterator, context)
