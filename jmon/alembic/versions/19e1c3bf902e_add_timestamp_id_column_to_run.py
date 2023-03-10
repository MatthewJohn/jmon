"""Add timestamp ID column to run

Revision ID: 19e1c3bf902e
Revises: c55d1e6736c9
Create Date: 2023-02-17 06:57:05.568695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '19e1c3bf902e'
down_revision = 'c55d1e6736c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('run', sa.Column('timestamp_id', sa.String(), nullable=True))
    
    # Set timestamp ID value for each run
    c = op.get_bind()
    res = c.execute("""
        SELECT check_id, timestamp FROM run
    """)
    for row in res:
        check_id, timestamp = row
        c.execute(
            sa.sql.text("""
                UPDATE run SET timestamp_id=:timestamp_id WHERE check_id=:check_id AND timestamp=:timestamp
            """),
            check_id=check_id, timestamp=timestamp, timestamp_id=timestamp.strftime('%Y-%m-%d_%H-%M-%S')
        )

    # Set disable nullable
    op.alter_column('run', 'timestamp',
            existing_type=postgresql.VARCHAR(),
            nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('run', 'timestamp_id')
    # ### end Alembic commands ###
