"""Update Coach Model Add Organization

Revision ID: c067a6cfbb32
Revises: ec254ebe7b73
Create Date: 2024-04-30 14:45:10.788591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c067a6cfbb32'
down_revision = 'ec254ebe7b73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles_coach', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organization', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'sport_organizations', ['organization'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profiles_coach', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('organization')

    # ### end Alembic commands ###