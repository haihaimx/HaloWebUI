"""Extend skill table for catalog and imports

Revision ID: 2c3d4e5f6a7b
Revises: f1a2b3c4d5e6
Create Date: 2026-03-17 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

revision = "2c3d4e5f6a7b"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if "skill" not in inspector.get_table_names():
        return

    columns = {c["name"] for c in inspector.get_columns("skill")}
    indexes = {idx["name"] for idx in inspector.get_indexes("skill")}

    if "source" not in columns:
        op.add_column(
            "skill",
            sa.Column("source", sa.Text(), nullable=False, server_default="manual"),
        )

    if "identifier" not in columns:
        op.add_column("skill", sa.Column("identifier", sa.Text(), nullable=True))

    if "source_url" not in columns:
        op.add_column("skill", sa.Column("source_url", sa.Text(), nullable=True))

    if "ix_skill_identifier" not in indexes:
        op.create_index("ix_skill_identifier", "skill", ["identifier"])


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if "skill" not in inspector.get_table_names():
        return

    columns = {c["name"] for c in inspector.get_columns("skill")}
    indexes = {idx["name"] for idx in inspector.get_indexes("skill")}

    if "ix_skill_identifier" in indexes:
        op.drop_index("ix_skill_identifier", "skill")

    if "source_url" in columns:
        op.drop_column("skill", "source_url")

    if "identifier" in columns:
        op.drop_column("skill", "identifier")

    if "source" in columns:
        op.drop_column("skill", "source")
