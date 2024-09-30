from flask import Blueprint, request, jsonify
from models import db, BookWarehouse

bookwarehouse_bp = Blueprint('bookwarehouse', __name__)


@bookwarehouse_bp.route('/book_warehouses', methods=['GET'])
def get_book_warehouses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'book_warehouse_id')
    order = request.args.get('order', 'asc')

    query = BookWarehouse.query

    if order == 'asc':
        query = query.order_by(getattr(BookWarehouse, sort_by).asc())
    else:
        query = query.order_by(getattr(BookWarehouse, sort_by).desc())

    book_warehouses = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'book_warehouses': [book_warehouse.serialize() for book_warehouse in book_warehouses.items],
        'total': book_warehouses.total,
        'pages': book_warehouses.pages,
        'current_page': book_warehouses.page
    })


@bookwarehouse_bp.route('/book_warehouses/<int:book_warehouse_id>', methods=['GET'])
def get_book_warehouse(book_warehouse_id):
    book_warehouse = BookWarehouse.query.filter_by(book_warehouse_id=book_warehouse_id).first()
    if not book_warehouse:
        return jsonify({'message': 'BookWarehouse not found'}), 404

    return jsonify(book_warehouse.serialize())


@bookwarehouse_bp.route('/book_warehouses', methods=['POST'])
def create_book_warehouse():
    data = request.get_json()
    if not data or not all(key in data for key in ['warehouse_id', 'book_id', 'book_amount']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_book_warehouse = BookWarehouse(
        warehouse_id=data['warehouse_id'],
        book_id=data['book_id'],
        book_amount=data['book_amount']
    )

    db.session.add(new_book_warehouse)
    db.session.commit()

    return jsonify({'message': 'BookWarehouse created successfully', 'book_warehouse_id': new_book_warehouse.book_warehouse_id}), 201

@bookwarehouse_bp.route('/book_warehouses/<int:book_warehouse_id>', methods=['PUT'])
def update_book_warehouse(book_warehouse_id):
    book_warehouse = BookWarehouse.query.filter_by(book_warehouse_id=book_warehouse_id).first()
    if not book_warehouse:
        return jsonify({'message': 'BookWarehouse not found'}), 404

    data = request.get_json()
    book_warehouse.warehouse_id = data.get('warehouse_id', book_warehouse.warehouse_id)
    book_warehouse.book_id = data.get('book_id', book_warehouse.book_id)
    book_warehouse.book_amount = data.get('book_amount', book_warehouse.book_amount)

    db.session.commit()
    return jsonify({'message': 'BookWarehouse updated successfully'})

@bookwarehouse_bp.route('/book_warehouses/<int:book_warehouse_id>', methods=['DELETE'])
def delete_book_warehouse(book_warehouse_id):
    book_warehouse = BookWarehouse.query.filter_by(book_warehouse_id=book_warehouse_id).first()
    if not book_warehouse:
        return jsonify({'message': 'BookWarehouse not found'}), 404

    db.session.delete(book_warehouse)
    db.session.commit()
    return jsonify({'message': 'BookWarehouse deleted successfully'})

