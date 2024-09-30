"""Initial migration.

Revision ID: c1d58cfcce94
Revises: 9afc71708a07
Create Date: 2024-06-15 16:02:10.932071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c1d58cfcce94'
down_revision = '9afc71708a07'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_deleted')

    # ### end Alembic commands ###
