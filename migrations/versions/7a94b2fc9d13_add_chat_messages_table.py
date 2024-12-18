"""Add chat_messages table

Revision ID: 7a94b2fc9d13
Revises: a52bb026274c
Create Date: 2024-12-17 09:07:42.344556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a94b2fc9d13'
down_revision = 'a52bb026274c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_username', sa.String(length=50), nullable=False),
    sa.Column('receiver_username', sa.String(length=50), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_messages')
    # ### end Alembic commands ###