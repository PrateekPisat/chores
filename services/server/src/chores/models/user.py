import uuid
from functools import cached_property

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chores.models.base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "chores"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    sub: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    picture: Mapped[str] = mapped_column(String, nullable=True)
    nickname: Mapped[str] = mapped_column(String, nullable=True)

    houses = relationship("HouseMember", back_populates="user")

    @cached_property
    def as_dict(self) -> dict[str, str]:
        return {
            "id": str(self.id),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "sub": self.sub,
            "picture": self.picture,
            "nickname": self.nickname,
        }

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"
