from collections.abc import Generator
from datetime import date, timedelta
from functools import cache

import grpc
import jwt
import pendulum
from google.protobuf.internal import enum_type_wrapper
from pydantic import ValidationError

from chores.config import Config
from chores.grpc_generated.chores_pb2 import Cadence, UpdateChorePayload
from chores.models.chore import Chore
from chores.models.user import User

CADENCE_MAP = {"DAILY": "days", "WEEKLY": "weeks", "MONTHLY": "months", "YEARLY": "years"}


@cache
def enum_mapper(enum_class: enum_type_wrapper.EnumTypeWrapper) -> dict:
    return dict(zip(enum_class.values(), enum_class.keys()))


def get_intervals(start_date: date, end_date: date, cadence: Cadence) -> Generator[date, None, None]:
    while start_date < end_date:
        start_date = start_date + timedelta(**{CADENCE_MAP[cadence]: 1})
        yield start_date


def distribution_needs_update(chore: Chore, request: UpdateChorePayload, enum_map: dict) -> bool:
    return (
        enum_map[request.cadence] != chore.cadence
        or request.start_date != chore.start_date
        or request.end_date != chore.end_date
    )


def get_token_payload(user: User, secret_key: str) -> str:
    return jwt.encode(
        {
            "sub": str(user.id),
            "name": user.name,
            "nickname": user.first_name,
            "exp": pendulum.now().add(days=1).timestamp(),
        },
        secret_key,
    )


def parse_errors(e: ValidationError) -> dict[str, str]:
    errors = {}
    for error in e.errors():
        field = error["loc"][0]
        if field not in errors:
            errors[field] = []
        errors[field].append(error["msg"])

    return {field: ".".join(error_list) for field, error_list in errors.items()}


def get_server_credentials(config: Config):
    return grpc.ssl_server_credentials(
        [
            (
                open(f"{config.certs_path}/localhost.key", "rb").read(),
                open(f"{config.certs_path}/localhost.crt", "rb").read(),
            )
        ],
    )
