from datetime import datetime

from flask import Blueprint, request, jsonify
from models import db, Order

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['GET'])
def get_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'order_id')
    order = request.args.get('order', 'asc')

    query = Order.query

    if order == 'asc':
        query = query.order_by(getattr(Order, sort_by).asc())
    else:
        query = query.order_by(getattr(Order, sort_by).desc())

    orders = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'orders': [order.serialize() for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': orders.page
    })

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    return jsonify(order.serialize())

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not all(key in data for key in ['user_id', 'order_number', 'status', 'total_price']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_order = Order(
        user_id=data['user_id'],
        order_number=data['order_number'],
        order_date=data.get('order_date', datetime.utcnow()),
        status=data['status'],
        total_price=data['total_price']
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.order_id}), 201

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    data = request.get_json()
    order.user_id = data.get('user_id', order.user_id)
    order.order_number = data.get('order_number', order.order_number)
    order.order_date = data.get('order_date', order.order_date)
    order.status = data.get('status', order.status)
    order.total_price = data.get('total_price', order.total_price)

    db.session.commit()
    return jsonify({'message': 'Order updated successfully'})

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully'})

