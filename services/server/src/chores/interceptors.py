from collections.abc import Callable

import jwt
from dependency_injector.wiring import inject, Provide
from grpc._server import _Context
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from chores.config import Config
from chores.db import Database
from chores.deps import Container
from chores.errors import Unauthenticated
from chores.models.user import TokenBlacklist


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
            jwt.decode(
                token, config.cryptography.secret_key, algorithms=["HS256"]
            )  # Replace with a better algo, check for expiration
        except ExpiredSignatureError:
            raise Unauthenticated("Token has expired")
        except InvalidTokenError:
            raise Unauthenticated("Invalid token")
        except StopIteration:
            raise Unauthenticated("Missing token")

        with database.session() as session:
            if session.query(TokenBlacklist).filter(TokenBlacklist.token == token).one_or_none():
                raise Unauthenticated("Token has expired")

        return method(request_or_iterator, context)
