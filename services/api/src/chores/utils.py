from functools import cache

from google.protobuf.internal import enum_type_wrapper


@cache
def enum_mapper(enum_class: enum_type_wrapper.EnumTypeWrapper) -> dict:
    return dict(zip(enum_class.values(), enum_class.keys()))
