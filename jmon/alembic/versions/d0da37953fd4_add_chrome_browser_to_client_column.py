"""Add chrome browser to client column

Revision ID: d0da37953fd4
Revises: 9d0524f5b53c
Create Date: 2023-02-21 07:10:07.206427

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'd0da37953fd4'
down_revision = '9d0524f5b53c'
branch_labels = None
depends_on = None


def upgrade() -> None:

    # Create a tempoary "clienttype" type, convert and drop the "old" type
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE clienttype ADD VALUE 'BROWSER_CHROME'")


def downgrade() -> None:
    op.execute("ALTER TYPE clienttype RENAME TO clienttype_old")
    op.execute("CREATE TYPE clienttype AS ENUM('STARTED', 'ACCEPTED')")
    op.execute((
        "ALTER TABLE check ALTER COLUMN client TYPE clienttype USING "
        "client::text::clienttype"
    ))
    op.execute("DROP TYPE clienttype_old")