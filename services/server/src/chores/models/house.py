from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chores.models.base import Base


class House(Base):
    __tablename__ = "house"
    __table_args__ = {"schema": "chores"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)

    members: Mapped[list[HouseMember]] = relationship("HouseMember", back_populates="house")
    chores = relationship("Chore", back_populates="house")


class HouseMember(Base):
    __tablename__ = "house_member"
    __table_args__ = {"schema": "chores"}

    house_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chores.house.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chores.user.id", ondelete="CASCADE"), primary_key=True
    )

    house: Mapped[House] = relationship("House", back_populates="members")
    user = relationship("User", back_populates="houses")
