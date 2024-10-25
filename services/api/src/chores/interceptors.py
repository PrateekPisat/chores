from collections.abc import Callable

import grpc
from grpc._server import _Context
from grpc_interceptor import ServerInterceptor
from grpc_interceptor.exceptions import GrpcException

from chores.errors import Unauthenticated


class ExceptionToStatusInterceptor(ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request_or_iterator,
        context: grpc.ServicerContext,
        method_name: str,
    ):
        try:
            return method(request_or_iterator, context)
        except GrpcException as e:
            context.set_code(e.status_code)
            context.set_details(e.details)
            raise


class AuthInterceptor(ServerInterceptor):
    def intercept(
        self,
        method: Callable,
        request_or_iterator,
        context: _Context,
        method_name: str,
    ):
        metadata = context.invocation_metadata()
        endpoint = method_name.split("/")[-1]

        # Check if metadata is empty
        if metadata is None or len(metadata) == 0:
            raise Unauthenticated("Missing Token")

        # Grab token
        token = get_token_from_metadata(metadata)

        # Use token to check permissions of user or service
        authed = check_user_auth(ENDPOINT_TO_PERM[endpoint], token)
        if not authed:
            raise Unauthenticated("You don't have access to this resource.")
        return method(request_or_iterator, context)
