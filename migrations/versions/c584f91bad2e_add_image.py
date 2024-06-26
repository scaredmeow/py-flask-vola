"""Add image

Revision ID: c584f91bad2e
Revises: edafbd6d3ed3
Create Date: 2024-05-07 14:18:45.727283

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c584f91bad2e'
down_revision = 'edafbd6d3ed3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.TEXT(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teams', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###
