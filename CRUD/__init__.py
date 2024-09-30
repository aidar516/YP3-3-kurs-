from flask import Blueprint
from .user_routes import user_bp
from .role_routes import role_bp
from .publisher_routes import publisher_bp
from .genre_routes import genre_bp
from .book_routes import book_bp
from .bookwarehouse_routes import bookwarehouse_bp
from .supplier_routes import supplier_bp
from .warehouse_routes import warehouse_bp
from .order_routes import order_bp
from .orderdetail_routes import orderdetail_bp
from .transaction_routes import transaction_bp
from .author_routes import author_bp
from .delivery_routes import delivery_bp

crud_bp = Blueprint('crud', __name__)

crud_bp.register_blueprint(user_bp, url_prefix='/users')
crud_bp.register_blueprint(role_bp, url_prefix='/roles')
crud_bp.register_blueprint(publisher_bp, url_prefix='/publishers')
crud_bp.register_blueprint(supplier_bp, url_prefix='/suppliers')
crud_bp.register_blueprint(book_bp, url_prefix='/books')
crud_bp.register_blueprint(bookwarehouse_bp, url_prefix='/bookwarehouses')
crud_bp.register_blueprint(warehouse_bp, url_prefix='/warehouses')
crud_bp.register_blueprint(order_bp, url_prefix='/orders')
crud_bp.register_blueprint(orderdetail_bp, url_prefix='/orderdetails')
crud_bp.register_blueprint(transaction_bp, url_prefix='/transactions')
crud_bp.register_blueprint(author_bp, url_prefix='/authors')
crud_bp.register_blueprint(delivery_bp, url_prefix='/deliveries')
crud_bp.register_blueprint(genre_bp, url_prefix='/genres')