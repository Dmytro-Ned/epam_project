"""empty message

Revision ID: 91b8633c51e1
Revises: 302f6fb4b907
Create Date: 2021-12-21 00:00:57.339784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b8633c51e1'
down_revision = '302f6fb4b907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('test_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'post', 'test', ['test_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'test_id')
    # ### end Alembic commands ###
