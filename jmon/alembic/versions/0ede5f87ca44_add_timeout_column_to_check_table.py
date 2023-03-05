"""Add timeout column to check table

Revision ID: 0ede5f87ca44
Revises: 782e7cd17d9c
Create Date: 2023-03-03 06:11:03.199399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ede5f87ca44'
down_revision = '782e7cd17d9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('check', sa.Column('timeout', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('check', 'timeout')
    # ### end Alembic commands ###
