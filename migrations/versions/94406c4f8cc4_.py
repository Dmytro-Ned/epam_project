"""empty message

Revision ID: 94406c4f8cc4
Revises: ec9c5caacd96
Create Date: 2021-12-23 20:05:13.972927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94406c4f8cc4'
down_revision = 'ec9c5caacd96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('last_question', sa.SmallInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('result', 'last_question')
    # ### end Alembic commands ###
