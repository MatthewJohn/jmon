"""Move run success column to status enum column

Revision ID: e686a7f6dfc1
Revises: 0ede5f87ca44
Create Date: 2023-03-03 06:41:01.236488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'e686a7f6dfc1'
down_revision = '0ede5f87ca44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    stepstatus_enum = postgresql.ENUM('NOT_RUN', 'RUNNING', 'SUCCESS', 'FAILED', 'TIMEOUT', 'INTERNAL_ERROR', name='stepstatus', create_type=False)
    stepstatus_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('run', sa.Column('status', sa.Enum('NOT_RUN', 'RUNNING', 'SUCCESS', 'FAILED', 'TIMEOUT', 'INTERNAL_ERROR', name='stepstatus'), nullable=True))

    c = op.get_bind()
    c.execute("""
        UPDATE run SET status='SUCCESS' WHERE success=true;
        UPDATE run SET status='FAILED' WHERE success=false;
        UPDATE run SET status='RUNNING' WHERE success IS NULL;
    """)

    op.drop_column('run', 'success')


def downgrade() -> None:
    op.add_column('run', sa.Column('success', sa.BOOLEAN(), autoincrement=False, nullable=True))

    c = op.get_bind()
    c.execute("""
        UPDATE run SET success=true WHERE status='SUCCESS';
        UPDATE run SET success=false WHERE status='FAILED';
    """)

    op.drop_column('run', 'status')

    stepstatus_enum = postgresql.ENUM('NOT_RUN', 'RUNNING', 'SUCCESS', 'FAILED', 'TIMEOUT', 'INTERNAL_ERROR', name='stepstatus', create_type=False)
    stepstatus_enum.drop(op.get_bind())
