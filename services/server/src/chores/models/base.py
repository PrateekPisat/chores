from typing import Any, ClassVar

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy_declarative_extensions import (
    declare_database,
    register_sqlalchemy_events,
    Schemas,
)

metadata = sqlalchemy.MetaData()


class Base(DeclarativeBase):
    metadata: ClassVar[sqlalchemy.MetaData] = metadata

    def __repr__(self) -> str:
        return self._repr(id=self.id)

    def _repr(self, **fields: dict[str, Any]) -> str:
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except sqlalchemy.orm.exc.DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


declare_database(Base.metadata, schemas=Schemas().are("chores"))
register_sqlalchemy_events(Base, schemas=True)


from chores.models import chore, house, user  # noqa: E402

__all__ = ["chore", "house", "user"]
