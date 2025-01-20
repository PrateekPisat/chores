from collections import defaultdict

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from grpc import StatusCode
from grpc._channel import _InactiveRpcError
from pydantic import ValidationError


def handle_validation_errors(_, error):
    body = defaultdict(list)

    for e in error.errors():
        key = ".".join([str(loc) for loc in e["loc"] if loc != "__root__"]).removeprefix("body.")
        if key == "body":
            key = ""

        body[key].append(e["msg"])

    return JSONResponse(status_code=422, content=body)


def handle_inactive_rpc_error(_, error: _InactiveRpcError):
    content = {"detail": error.details()}
    match error.code():
        case StatusCode.NOT_FOUND:
            return JSONResponse(status_code=404, content=content)
        case StatusCode.INVALID_ARGUMENT:
            return JSONResponse(status_code=400, content=content)
        case StatusCode.PERMISSION_DENIED:
            return JSONResponse(status_code=403, content=content)
        case StatusCode.UNAUTHENTICATED:
            return JSONResponse(status_code=401, content=content)
        case _:
            return JSONResponse(status_code=503, content=content)


error_handlers = [
    (_InactiveRpcError, handle_inactive_rpc_error),
    # 422
    (ValidationError, handle_validation_errors),
    (RequestValidationError, handle_validation_errors),
]
