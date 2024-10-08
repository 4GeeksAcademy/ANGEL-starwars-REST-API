"""empty message

Revision ID: 38e60f0c976d
Revises: 3b174bf6ca0a
Create Date: 2024-08-29 22:55:17.837353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '38e60f0c976d'
down_revision = '3b174bf6ca0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('people_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('planet_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('film_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorites_userId_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_planetId_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_filmId_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_peopleId_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])
        batch_op.create_foreign_key(None, 'planet', ['planet_id'], ['id'])
        batch_op.create_foreign_key(None, 'film', ['film_id'], ['id'])
        batch_op.drop_column('planetId')
        batch_op.drop_column('filmId')
        batch_op.drop_column('peopleId')
        batch_op.drop_column('userId')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userId', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('peopleId', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('filmId', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('planetId', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorites_peopleId_fkey', 'people', ['peopleId'], ['id'])
        batch_op.create_foreign_key('favorites_filmId_fkey', 'film', ['filmId'], ['id'])
        batch_op.create_foreign_key('favorites_planetId_fkey', 'planet', ['planetId'], ['id'])
        batch_op.create_foreign_key('favorites_userId_fkey', 'user', ['userId'], ['id'])
        batch_op.drop_column('film_id')
        batch_op.drop_column('planet_id')
        batch_op.drop_column('people_id')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
