import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from chores.models.base import Base


class House(Base):
    __tablename__ = "house"
    __table_args__ = {"schema": "chores"}

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String, nullable=False)

    members = relationship("HouseMember", back_populates="house")


class HouseMember(Base):
    __tablename__ = "house_member"
    __table_args__ = {"schema": "chores"}

    house_id = mapped_column(UUID(as_uuid=True), ForeignKey("chores.house.id"), primary_key=True)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("chores.user.id"), primary_key=True)

    house = relationship("House", back_populates="members")
    user = relationship("User", back_populates="houses")
