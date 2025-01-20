import grpc
from grpc_interceptor.exceptions import GrpcException


class NotFound(GrpcException):
    status_code = grpc.StatusCode.NOT_FOUND


class AlreadyExists(GrpcException):
    status_code = grpc.StatusCode.ALREADY_EXISTS


class Unauthenticated(GrpcException):
    status_code = grpc.StatusCode.UNAUTHENTICATED


class PermissionDenied(GrpcException):
    status_code = grpc.StatusCode.PERMISSION_DENIED
