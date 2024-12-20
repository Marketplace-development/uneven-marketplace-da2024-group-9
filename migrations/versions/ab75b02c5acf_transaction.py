"""transaction

Revision ID: ab75b02c5acf
Revises: f0ac4407898c
Create Date: 2024-12-18 12:02:54.014962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab75b02c5acf'
down_revision = 'f0ac4407898c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('listing_id', sa.Integer(), nullable=False),
    sa.Column('student_username', sa.String(length=80), nullable=False),
    sa.Column('technician_username', sa.String(length=80), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.drop_column('status')
        batch_op.drop_column('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('status', sa.VARCHAR(length=20), autoincrement=False, nullable=True))

    op.drop_table('transactions')
    # ### end Alembic commands ###
