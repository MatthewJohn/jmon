"""Add table for environment and add foreign key from check. Replace check name primary key with unique constraint across name and environment id

Revision ID: 782e7cd17d9c
Revises: 3ae8d25812d5
Create Date: 2023-02-24 07:20:20.433382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '782e7cd17d9c'
down_revision = '3ae8d25812d5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('environment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('check', sa.Column('environment_id', sa.Integer(), nullable=True))
    op.create_unique_constraint('uc_name_environment_id', 'check', ['name', 'environment_id'])
    op.create_foreign_key('fk_check_environment_id_environment_id', 'check', 'environment', ['environment_id'], ['id'])

    bind = op.get_bind()
    # Create default environment
    bind.execute("""
        INSERT INTO public.environment(id, name) VALUES(1, 'default')
    """)
    # Update all checks to default environment
    bind.execute("""
        UPDATE public.check SET environment_id=1
    """)

    # Remove nullable flag from check.environment_id
    op.alter_column('check', sa.Column('environment_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_check_environment_id_environment_id', 'check', type_='foreignkey')
    op.drop_constraint('uc_name_environment_id', 'check', type_='unique')
    op.drop_column('check', 'environment_id')
    op.drop_table('environment')
    # ### end Alembic commands ###