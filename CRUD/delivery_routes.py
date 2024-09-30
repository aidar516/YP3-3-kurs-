from flask import Blueprint, request, jsonify
from models import db, Delivery

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/deliveries', methods=['GET'])
def get_deliveries():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'delivery_id')
    order = request.args.get('order', 'asc')

    query = Delivery.query

    if order == 'asc':
        query = query.order_by(getattr(Delivery, sort_by).asc())
    else:
        query = query.order_by(getattr(Delivery, sort_by).desc())

    deliveries = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'deliveries': [delivery.serialize() for delivery in deliveries.items],
        'total': deliveries.total,
        'pages': deliveries.pages,
        'current_page': deliveries.page
    })

@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['GET'])
def get_delivery(delivery_id):
    delivery = Delivery.query.filter_by(delivery_id=delivery_id).first()
    if not delivery:
        return jsonify({'message': 'Delivery not found'}), 404

    return jsonify(delivery.serialize())

@delivery_bp.route('/deliveries', methods=['POST'])
def create_delivery():
    data = request.get_json()
    if not data or not all(key in data for key in ['supplier_id', 'warehouse_id', 'book_id', 'book_amount']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_delivery = Delivery(
        supplier_id=data['supplier_id'],
        warehouse_id=data['warehouse_id'],
        book_id=data['book_id'],
        book_amount=data['book_amount']
    )

    db.session.add(new_delivery)
    db.session.commit()

    return jsonify({'message': 'Delivery created successfully', 'delivery_id': new_delivery.delivery_id}), 201

@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['PUT'])
def update_delivery(delivery_id):
    delivery = Delivery.query.filter_by(delivery_id=delivery_id).first()
    if not delivery:
        return jsonify({'message': 'Delivery not found'}), 404

    data = request.get_json()
    delivery.supplier_id = data.get('supplier_id', delivery.supplier_id)
    delivery.warehouse_id = data.get('warehouse_id', delivery.warehouse_id)
    delivery.book_id = data.get('book_id', delivery.book_id)
    delivery.book_amount = data.get('book_amount', delivery.book_amount)

    db.session.commit()
    return jsonify({'message': 'Delivery updated successfully'})

@delivery_bp.route('/deliveries/<int:delivery_id>', methods=['DELETE'])
def delete_delivery(delivery_id):
    delivery = Delivery.query.filter_by(delivery_id=delivery_id).first()
    if not delivery:
        return jsonify({'message': 'Delivery not found'}), 404

    db.session.delete(delivery)
    db.session.commit()
    return jsonify({'message': 'Delivery deleted successfully'})

