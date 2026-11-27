"""Make user.sub unique.

Revision ID: b7e4c1a92d08
Revises: 5eb5d23dce76
Create Date: 2026-04-11 12:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

revision: str = "b7e4c1a92d08"
down_revision: str | None = "5eb5d23dce76"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index(op.f("ix_chores_user_sub"), table_name="user", schema="chores")
    op.create_index(op.f("ix_chores_user_sub"), "user", ["sub"], unique=True, schema="chores")


def downgrade() -> None:
    op.drop_index(op.f("ix_chores_user_sub"), table_name="user", schema="chores")
    op.create_index(op.f("ix_chores_user_sub"), "user", ["sub"], unique=False, schema="chores")
