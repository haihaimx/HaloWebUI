"""Drop feedback table

Revision ID: 9b5e0d6f4a71
Revises: 3781e22d8b01
Create Date: 2026-02-02 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = "9b5e0d6f4a71"
down_revision = "3781e22d8b01"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    if "feedback" in inspector.get_table_names():
        op.drop_table("feedback")


def downgrade():
    op.create_table(
        "feedback",
        sa.Column("id", sa.Text(), primary_key=True),
        sa.Column("user_id", sa.Text(), nullable=True),
        sa.Column("version", sa.BigInteger(), default=0),
        sa.Column("type", sa.Text(), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column("meta", sa.JSON(), nullable=True),
        sa.Column("snapshot", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.BigInteger(), nullable=False),
        sa.Column("updated_at", sa.BigInteger(), nullable=False),
    )
