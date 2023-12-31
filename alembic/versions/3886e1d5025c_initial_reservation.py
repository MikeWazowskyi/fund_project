"""Initial reservation

Revision ID: 3886e1d5025c
Revises: 685a511d18c0
Create Date: 2023-07-13 19:46:19.804511

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '3886e1d5025c'
down_revision = '685a511d18c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fully_invested', sa.Boolean(), nullable=True))

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_column('fully_invested')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fully_invested', sa.BOOLEAN(), nullable=True))

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_column('fully_invested')

    # ### end Alembic commands ###
