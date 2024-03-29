"""empty message

Revision ID: 46fdfdd20657
Revises: 
Create Date: 2019-12-09 12:20:29.317682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46fdfdd20657'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('airline',
    sa.Column('iata', sa.String(length=2), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('iata')
    )
    op.create_table('airport',
    sa.Column('iata', sa.String(length=3), nullable=False),
    sa.Column('name', sa.String(length=75), nullable=False),
    sa.Column('city', sa.String(length=75), nullable=False),
    sa.Column('country', sa.String(length=50), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('time_zone', sa.String(length=60), nullable=False),
    sa.Column('dst', sa.String(length=1), nullable=False),
    sa.PrimaryKeyConstraint('iata')
    )
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('session', sa.String(length=50), nullable=True),
    sa.CheckConstraint("email LIKE '%_@_%._%'"),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('trip',
    sa.Column('tid', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('trip_name', sa.String(length=30), nullable=False),
    sa.Column('color', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['uid'], ['user.uid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('tid')
    )
    op.create_table('flight',
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.Column('tid', sa.Integer(), nullable=False),
    sa.Column('airline_iata', sa.String(length=2), nullable=True),
    sa.Column('flight_num', sa.Integer(), nullable=True),
    sa.Column('depart_iata', sa.String(length=3), nullable=False),
    sa.Column('arrival_iata', sa.String(length=3), nullable=False),
    sa.Column('depart_datetime', sa.DateTime(), nullable=False),
    sa.Column('arrival_datetime', sa.DateTime(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('mileage', sa.Integer(), nullable=False),
    sa.CheckConstraint('duration > 0'),
    sa.CheckConstraint('flight_num > 0'),
    sa.CheckConstraint('mileage > 0'),
    sa.ForeignKeyConstraint(['airline_iata'], ['airline.iata'], ),
    sa.ForeignKeyConstraint(['arrival_iata'], ['airport.iata'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['depart_iata'], ['airport.iata'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tid'], ['trip.tid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('fid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flight')
    op.drop_table('trip')
    op.drop_table('user')
    op.drop_table('airport')
    op.drop_table('airline')
    # ### end Alembic commands ###
