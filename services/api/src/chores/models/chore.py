import uuid

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

from chores.models.base import Base


class Chore(Base):
    __tablename__ = "chore"
    __table_args__ = {"schema": "chores"}

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    cadence = mapped_column(String, nullable=False)


class Task(Base):
    __tablename__ = "task"
    __table_args__ = {"schema": "chores"}

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chore_id = mapped_column(UUID(as_uuid=True), ForeignKey("chores.chore.id"), nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("chores.user.id"), nullable=False)
    due_date = mapped_column(Date, nullable=False)
    completed_at = mapped_column(DateTime(timezone=True), nullable=True)

    chore = relationship("Chore")
    user = relationship("User")


class ChoreDistribution(Base):
    __tablename__ = "chore_distribution"
    __table_args__ = {"schema": "chores"}

    chore_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("chores.chore.id"), nullable=False, primary_key=True
    )
    user_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("chores.user.id"), nullable=False, primary_key=True
    )
    start_date = mapped_column(Date, nullable=False)
    end_date = mapped_column(Date, nullable=False)

    chore = relationship("Chore")
    user = relationship("User")
