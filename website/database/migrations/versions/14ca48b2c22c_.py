"""empty message

Revision ID: 14ca48b2c22c
Revises: 2a1c4e2cfe94
Create Date: 2024-03-30 17:47:25.169009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14ca48b2c22c'
down_revision = '2a1c4e2cfe94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_playlists', schema=None) as batch_op:
        batch_op.drop_constraint('users_playlists_playlist_id_key', type_='unique')
        batch_op.create_unique_constraint(None, ['playlist_id', 'user_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users_playlists', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_unique_constraint('users_playlists_playlist_id_key', ['playlist_id'])

    # ### end Alembic commands ###