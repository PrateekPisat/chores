from functools import cache

import pendulum
from google.protobuf.internal import enum_type_wrapper

from chores.grpc_generated.chores_pb2 import Cadence

CADENCE_MAP = {Cadence.DAILY: "days", Cadence.WEEKLY: "weeks", Cadence.MONTHLY: "months", Cadence.YEARLY: "years"}


@cache
def enum_mapper(enum_class: enum_type_wrapper.EnumTypeWrapper) -> dict:
    return dict(zip(enum_class.values(), enum_class.keys()))


@cache
def get_intervals(start_date: pendulum.Date, end_date: pendulum.Date, cadence: Cadence):
    while start_date <= end_date:
        start_date = start_date.add(**{CADENCE_MAP[cadence]: 1})
        yield start_date
