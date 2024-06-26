"""Add new columns

Revision ID: 4edd0fd52842
Revises: c584f91bad2e
Create Date: 2024-05-14 20:43:39.618160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4edd0fd52842'
down_revision = 'c584f91bad2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('team_id', sa.Integer(), nullable=True),
    sa.Column('stats_key', sa.TEXT(), nullable=True),
    sa.Column('stats_value', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_profiles.uid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('player_stats')
    # ### end Alembic commands ###
