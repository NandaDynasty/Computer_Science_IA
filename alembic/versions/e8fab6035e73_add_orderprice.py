"""add orderprice

Revision ID: e8fab6035e73
Revises: bd5fe9e49643
Create Date: 2023-07-26 22:02:31.127770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8fab6035e73'
down_revision = 'bd5fe9e49643'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderprice',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orderprice')
    # ### end Alembic commands ###
