"""Initial migration.

Revision ID: 0a1b5a02e5fb
Revises: 
Create Date: 2024-06-14 18:43:48.993166

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0a1b5a02e5fb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=30), nullable=True),
    sa.Column('author_surname', sa.String(length=30), nullable=True),
    sa.Column('biography', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('author_id')
    )
    op.create_table('genres',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table('publishers',
    sa.Column('publisher_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('address', sa.String(length=30), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('publisher_id')
    )
    op.create_table('roles',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('suppliers',
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('supplier_name', sa.String(length=30), nullable=True),
    sa.Column('address', sa.String(length=30), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('supplier_id')
    )
    op.create_table('warehouses',
    sa.Column('warehouse_id', sa.Integer(), nullable=False),
    sa.Column('warehouse_name', sa.String(length=30), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.PrimaryKeyConstraint('warehouse_id')
    )
    op.create_table('books',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('book_name', sa.String(length=255), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('publisher_id', sa.Integer(), nullable=True),
    sa.Column('price', mysql.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('year', sa.DateTime(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.author_id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genres.genre_id'], ),
    sa.ForeignKeyConstraint(['publisher_id'], ['publishers.publisher_id'], ),
    sa.PrimaryKeyConstraint('book_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=30), nullable=True),
    sa.Column('user_surname', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=12), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('salt', sa.String(length=255), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.role_id'], ),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('book_warehouses',
    sa.Column('book_warehouse_id', sa.Integer(), nullable=False),
    sa.Column('warehouse_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('book_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.warehouse_id'], ),
    sa.PrimaryKeyConstraint('book_warehouse_id')
    )
    op.create_table('deliveries',
    sa.Column('delivery_id', sa.Integer(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('warehouse_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('book_amount', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.supplier_id'], ),
    sa.ForeignKeyConstraint(['warehouse_id'], ['warehouses.warehouse_id'], ),
    sa.PrimaryKeyConstraint('delivery_id')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=10), nullable=True),
    sa.Column('total_price', mysql.DECIMAL(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('order_details',
    sa.Column('order_detail_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('book_amount', sa.Integer(), nullable=True),
    sa.Column('unit_price', mysql.DECIMAL(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('order_detail_id')
    )
    op.create_table('transactions',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('transaction_date', sa.DateTime(), nullable=True),
    sa.Column('transaction_amount', mysql.DECIMAL(precision=10, scale=2), nullable=True),
    sa.Column('transaction_type', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('order_details')
    op.drop_table('orders')
    op.drop_table('deliveries')
    op.drop_table('book_warehouses')
    op.drop_table('users')
    op.drop_table('books')
    op.drop_table('warehouses')
    op.drop_table('suppliers')
    op.drop_table('roles')
    op.drop_table('publishers')
    op.drop_table('genres')
    op.drop_table('authors')
    # ### end Alembic commands ###
