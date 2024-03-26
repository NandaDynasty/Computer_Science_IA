"""create productstock

Revision ID: 80d35fa300c9
Revises: c3ac15ac5701
Create Date: 2024-02-13 09:05:50.928365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80d35fa300c9'
down_revision = 'c3ac15ac5701'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_stock',
    sa.Column('product_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=False),
    sa.Column('current_stock', sa.Integer(), nullable=False),
    sa.Column('minimum_stock', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_stock')
    # ### end Alembic commands ###
