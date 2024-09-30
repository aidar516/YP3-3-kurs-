from flask import Blueprint, request, jsonify
from models import db, OrderDetail

orderdetail_bp = Blueprint('orderdetail', __name__)

@orderdetail_bp.route('/order_details', methods=['GET'])
def get_order_details():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'order_detail_id')
    order = request.args.get('order', 'asc')

    query = OrderDetail.query

    if order == 'asc':
        query = query.order_by(getattr(OrderDetail, sort_by).asc())
    else:
        query = query.order_by(getattr(OrderDetail, sort_by).desc())

    order_details = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'order_details': [order_detail.serialize() for order_detail in order_details.items],
        'total': order_details.total,
        'pages': order_details.pages,
        'current_page': order_details.page
    })

@orderdetail_bp.route('/order_details/<int:order_detail_id>', methods=['GET'])
def get_order_detail(order_detail_id):
    order_detail = OrderDetail.query.filter_by(order_detail_id=order_detail_id).first()
    if not order_detail:
        return jsonify({'message': 'OrderDetail not found'}), 404

    return jsonify(order_detail.serialize())

@orderdetail_bp.route('/order_details', methods=['POST'])
def create_order_detail():
    data = request.get_json()
    if not data or not all(key in data for key in ['order_id', 'book_id', 'book_amount', 'unit_price']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_order_detail = OrderDetail(
        order_id=data['order_id'],
        book_id=data['book_id'],
        book_amount=data['book_amount'],
        unit_price=data['unit_price']
    )

    db.session.add(new_order_detail)
    db.session.commit()

    return jsonify({'message': 'OrderDetail created successfully', 'order_detail_id': new_order_detail.order_detail_id}), 201

@orderdetail_bp.route('/order_details/<int:order_detail_id>', methods=['PUT'])
def update_order_detail(order_detail_id):
    order_detail = OrderDetail.query.filter_by(order_detail_id=order_detail_id).first()
    if not order_detail:
        return jsonify({'message': 'OrderDetail not found'}), 404

    data = request.get_json()
    order_detail.order_id = data.get('order_id', order_detail.order_id)
    order_detail.book_id = data.get('book_id', order_detail.book_id)
    order_detail.book_amount = data.get('book_amount', order_detail.book_amount)
    order_detail.unit_price = data.get('unit_price', order_detail.unit_price)

    db.session.commit()
    return jsonify({'message': 'OrderDetail updated successfully'})

@orderdetail_bp.route('/order_details/<int:order_detail_id>', methods=['DELETE'])
def delete_order_detail(order_detail_id):
    order_detail = OrderDetail.query.filter_by(order_detail_id=order_detail_id).first()
    if not order_detail:
        return jsonify({'message': 'OrderDetail not found'}), 404

    db.session.delete(order_detail)
    db.session.commit()
    return jsonify({'message': 'OrderDetail deleted successfully'})