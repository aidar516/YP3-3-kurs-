from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import DECIMAL
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

db = SQLAlchemy()

class Role(db.Model):
    __tablename__ = 'roles'
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    users = db.relationship("User", back_populates="role")

    def __str__(self):
        return self.role_name

    def serialize(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'is_deleted': self.is_deleted
        }

class Publisher(db.Model):
    __tablename__ = 'publishers'
    publisher_id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    books = db.relationship("Book", back_populates="publisher")

    def __str__(self):
        return self.publisher_name

    def serialize(self):
        return {
            'publisher_id': self.publisher_id,
            'publisher_name': self.publisher_name,
            'address': self.address,
            'phone': self.phone,
            'website': self.website,
            'is_deleted': self.is_deleted,
        }

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(30), nullable=True)
    description = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    books = db.relationship("Book", back_populates="genre")

    def __str__(self):
        return self.genre_name

    def serialize(self):
        return {
            'genre_id': self.genre_id,
            'genre_name': self.genre_name,
            'description': self.description,
            'is_deleted': self.is_deleted,
        }

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(30), nullable=True)
    author_surname = db.Column(db.String(30), nullable=True)
    biography = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    books = db.relationship("Book", back_populates="author")

    def __str__(self):
        return f"{self.author_name} {self.author_surname}"

    def serialize(self):
        return {
            'author_id': self.author_id,
            'author_name': self.author_name,
            'author_surname': self.author_surname,
            'biography': self.biography,
            'is_deleted': self.is_deleted,
        }

class Warehouse(db.Model):
    __tablename__ = 'warehouses'
    warehouse_id = db.Column(db.Integer, primary_key=True)
    warehouse_name = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    book_warehouses = db.relationship("BookWarehouse", back_populates="warehouse")
    deliveries = db.relationship("Delivery", back_populates="warehouse")

    def __str__(self):
        return self.warehouse_name

    def serialize(self):
        return {
            'warehouse_id': self.warehouse_id,
            'warehouse_name': self.warehouse_name,
            'phone': self.phone,
            'is_deleted': self.is_deleted,
        }

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(30), nullable=True)
    address = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(12), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    deliveries = db.relationship("Delivery", back_populates="supplier")

    def __str__(self):
        return self.supplier_name

    def serialize(self):
        return {
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier_name,
            'address': self.address,
            'phone': self.phone,
            'is_deleted': self.is_deleted,
        }

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(50), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    token = db.Column(db.String(255), nullable=True)
    salt = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    role = db.relationship("Role", back_populates="users")
    orders = db.relationship("Order", back_populates="user")

    def __str__(self):
        return f"{self.user_name} {self.user_surname}"

    def serialize(self):
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'role_id': self.role_id,
            'is_deleted': self.is_deleted,
        }

    def set_password(self, password):
        self.salt = secrets.token_hex(8)  # Генерируем случайную соль
        self.password_hash = generate_password_hash(password + self.salt)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + self.salt)

    def generate_token(self):
        self.token = secrets.token_urlsafe(32)  # Генерируем случайный токен


class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('publishers.publisher_id'))
    price = db.Column(DECIMAL(10, 2))
    year = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255), nullable=True)
    author = db.relationship("Author", back_populates="books")
    genre = db.relationship("Genre", back_populates="books")
    publisher = db.relationship("Publisher", back_populates="books")
    order_details = db.relationship("OrderDetail", back_populates="book")
    book_warehouses = db.relationship("BookWarehouse", back_populates="book")
    deliveries = db.relationship("Delivery", back_populates="book")

    def __str__(self):
        return self.book_name

    def serialize(self):
        return {
            'book_id': self.book_id,
            'book_name': self.book_name,
            'author': self.author.serialize(),
            'genre': self.genre.serialize(),
            'publisher': self.publisher.serialize(),
            'price': str(self.price),
            'year': self.year.isoformat(),
            'description': self.description,
            'is_deleted': self.is_deleted,
            'image': self.image,
        }

class Transaction(db.Model):
    __tablename__ = 'transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    transaction_amount = db.Column(DECIMAL(10, 2))
    transaction_type = db.Column(db.String(30), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)
    order = db.relationship("Order", back_populates="transactions")

    def __str__(self):
        return str(self.transaction_id)

    def serialize(self):
        return {
            'transaction_id': self.transaction_id,
            'order_id': self.order_id,
            'transaction_date': self.transaction_date.isoformat(),
            'transaction_amount': str(self.transaction_amount),
            'transaction_type': self.transaction_type,
            'is_deleted': self.is_deleted,
        }

class BookWarehouse(db.Model):
    __tablename__ = 'book_warehouses'
    book_warehouse_id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    book_amount = db.Column(db.Integer)
    is_deleted = db.Column(db.Boolean, default=False)
    warehouse = db.relationship("Warehouse", back_populates="book_warehouses")
    book = db.relationship("Book", back_populates="book_warehouses")

    def __str__(self):
        return f"{self.book.book_name} - {self.warehouse.warehouse_name}"

    def serialize(self):
        return {
            'book_warehouse_id': self.book_warehouse_id,
            'warehouse': self.warehouse.serialize(),
            'book': self.book.serialize(),
            'book_amount': self.book_amount,
            'is_deleted': self.is_deleted,
        }

class Delivery(db.Model):
    __tablename__ = 'deliveries'
    delivery_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.warehouse_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    book_amount = db.Column(db.Integer)
    delivery_date = db.Column(db.DateTime, default=datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
    supplier = db.relationship("Supplier", back_populates="deliveries")
    warehouse = db.relationship("Warehouse", back_populates="deliveries")
    book = db.relationship("Book", back_populates="deliveries")

    def __str__(self):
        return f"{self.book.book_name} - {self.warehouse.warehouse_name} - {self.supplier.supplier_name}"

    def serialize(self):
        return {
            'delivery_id': self.delivery_id,
            'supplier': self.supplier.serialize(),
            'warehouse': self.warehouse.serialize(),
            'book': self.book.serialize(),
            'book_amount': self.book_amount,
            'delivery_date': self.delivery_date.isoformat(),
            'is_deleted': self.is_deleted,
        }


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    order_detail_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    book_amount = db.Column(db.Integer)
    unit_price = db.Column(DECIMAL(10, 2))
    is_deleted = db.Column(db.Boolean, default=False)
    order = db.relationship("Order", back_populates="order_details")
    book = db.relationship("Book", back_populates="order_details")

    def __str__(self):
        return f"{self.book.book_name} - {self.order.order_number}"

    def serialize(self):
        return {
            'order_detail_id': self.order_detail_id,
            'order': self.order.serialize(),
            'book': self.book.serialize(),
            'book_amount': self.book_amount,
            'unit_price': str(self.unit_price),
            'is_deleted': self.is_deleted,
        }

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    order_number = db.Column(db.Integer)
    order_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(10), nullable=True)
    total_price = db.Column(DECIMAL(10, 2))
    is_deleted = db.Column(db.Boolean, default=False)
    user = db.relationship("User", back_populates="orders")
    transactions = db.relationship("Transaction", back_populates="order")
    order_details = db.relationship("OrderDetail", back_populates="order")

    def __str__(self):
        return str(self.order_number)


    def serialize(self):
        return {
            'order_id': self.order_id,
            'user': self.user.serialize(),
            'order_number': self.order_number,
            'order_date': self.order_date.isoformat(),
            'status': self.status,
            'total_price': str(self.total_price),
            'is_deleted': self.is_deleted,
        }