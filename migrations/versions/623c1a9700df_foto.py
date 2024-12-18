"""foto

Revision ID: 623c1a9700df
Revises: 0d510cc3a261
Create Date: 2024-12-18 13:27:27.673416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '623c1a9700df'
down_revision = '0d510cc3a261'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    def upgrade():
        op.execute('ALTER TABLE listings ALTER COLUMN photo TYPE BYTEA USING photo::bytea')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('listings', schema=None) as batch_op:
        batch_op.alter_column('photo',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###
