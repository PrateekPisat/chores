import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chores.models.base import Base


class Chore(Base):
    __tablename__ = "chore"
    __table_args__ = {"schema": "chores"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    cadence: Mapped[str] = mapped_column(String, nullable=False)


class Task(Base):
    __tablename__ = "task"
    __table_args__ = {"schema": "chores"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chore_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chores.chore.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chores.user.id"), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    chore: Mapped[Chore] = relationship("Chore")
    user = relationship("User")


class ChoreDistribution(Base):
    __tablename__ = "chore_distribution"
    __table_args__ = {"schema": "chores"}

    chore_id = mapped_column(UUID(as_uuid=True), ForeignKey("chores.chore.id"), nullable=False, primary_key=True)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("chores.user.id"), nullable=False, primary_key=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)

    chore: Mapped[Chore] = relationship("Chore")
    user = relationship("User")
