import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from chores.models.base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "chores"}

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = mapped_column(String, nullable=False)
    last_name = mapped_column(String, nullable=False)
    email = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)

    houses = relationship("HouseMember", back_populates="user")
