"""Fully invested field added to Donation model

Revision ID: 0559a636066d
Revises: 3886e1d5025c
Create Date: 2023-07-15 17:02:45.938805

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0559a636066d'
down_revision = '3886e1d5025c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.create_unique_constraint('name', ['name'])

    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('fully_invested', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation', schema=None) as batch_op:
        batch_op.drop_column('fully_invested')

    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_constraint('name', type_='unique')

    # ### end Alembic commands ###
