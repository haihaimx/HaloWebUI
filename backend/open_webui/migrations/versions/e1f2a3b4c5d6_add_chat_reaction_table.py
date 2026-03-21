"""Add chat_reaction table for message emoji reactions

Revision ID: e1f2a3b4c5d6
Revises: d1e2f3a4b5c6
Create Date: 2026-03-07 21:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

revision = "e1f2a3b4c5d6"
down_revision = "d1e2f3a4b5c6"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if "chat_reaction" not in inspector.get_table_names():
        op.create_table(
            "chat_reaction",
            sa.Column("id", sa.Text(), nullable=False, primary_key=True),
            sa.Column("user_id", sa.Text(), nullable=False),
            sa.Column("chat_id", sa.Text(), nullable=False),
            sa.Column("message_id", sa.Text(), nullable=False),
            sa.Column("name", sa.Text(), nullable=False),
            sa.Column("created_at", sa.BigInteger(), nullable=False),
        )

        op.create_index(
            "ix_chat_reaction_chat_message",
            "chat_reaction",
            ["chat_id", "message_id"],
        )


def downgrade():
    op.drop_index("ix_chat_reaction_chat_message", table_name="chat_reaction")
    op.drop_table("chat_reaction")
