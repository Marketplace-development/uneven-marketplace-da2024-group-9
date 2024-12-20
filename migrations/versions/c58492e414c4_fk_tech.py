"""FK tech

Revision ID: c58492e414c4
Revises: 9ce243fb4c52
Create Date: 2024-12-18 16:49:29.874714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c58492e414c4'
down_revision = '9ce243fb4c52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('technician_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'technicians', ['technician_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('transactions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('technician_id')

    # ### end Alembic commands ###
