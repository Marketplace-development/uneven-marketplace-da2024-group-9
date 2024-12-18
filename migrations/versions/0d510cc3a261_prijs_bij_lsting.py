"""prijs bij lsting

Revision ID: 0d510cc3a261
Revises: ab75b02c5acf
Create Date: 2024-12-18 12:13:46.430612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d510cc3a261'
down_revision = 'ab75b02c5acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.drop_column('price')

    # ### end Alembic commands ###