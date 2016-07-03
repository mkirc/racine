"""Added column for inheriting data

Revision ID: 5ae6e19e0a7b
Revises: 17c32bd785e3
Create Date: 2016-07-03 18:38:19.972367

"""

# revision identifiers, used by Alembic.
revision = '5ae6e19e0a7b'
down_revision = '17c32bd785e3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('heir_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('users', 'users', ['heir_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_constraint('users', type_='foreignkey')
        batch_op.drop_column('heir_id')
    ### end Alembic commands ###
