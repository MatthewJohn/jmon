"""Add screenshot_on_error column to Check

Revision ID: 3bc55597348d
Revises: 03ea2fc77d60
Create Date: 2023-02-15 16:56:14.694538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bc55597348d'
down_revision = '03ea2fc77d60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('check', sa.Column('screenshot_on_error', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('check', 'screenshot_on_error')
    # ### end Alembic commands ###
