from flask import Blueprint, request, jsonify
from models import db, Supplier

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/', methods=['GET'])
def get_suppliers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'supplier_id')
    order = request.args.get('order', 'asc')

    query = Supplier.query

    if order == 'asc':
        query = query.order_by(getattr(Supplier, sort_by).asc())
    else:
        query = query.order_by(getattr(Supplier, sort_by).desc())

    suppliers = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'suppliers': [supplier.serialize() for supplier in suppliers.items],
        'total': suppliers.total,
        'pages': suppliers.pages,
        'current_page': suppliers.page
    })

@supplier_bp.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = Supplier.query.filter_by(supplier_id=supplier_id).first()
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    return jsonify(supplier.serialize())

@supplier_bp.route('/', methods=['POST'])
def create_supplier():
    data = request.get_json()
    if not data or not all(key in data for key in ['supplier_name', 'address', 'phone']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_supplier = Supplier(
        supplier_name=data['supplier_name'],
        address=data['address'],
        phone=data['phone']
    )

    db.session.add(new_supplier)
    db.session.commit()

    return jsonify({'message': 'Supplier created successfully', 'supplier_id': new_supplier.supplier_id}), 201

@supplier_bp.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier = Supplier.query.filter_by(supplier_id=supplier_id).first()
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    data = request.get_json()
    supplier.supplier_name = data.get('supplier_name', supplier.supplier_name)
    supplier.address = data.get('address', supplier.address)
    supplier.phone = data.get('phone', supplier.phone)

    db.session.commit()
    return jsonify({'message': 'Supplier updated successfully'})

@supplier_bp.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = Supplier.query.filter_by(supplier_id=supplier_id).first()
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    db.session.delete(supplier)
    db.session.commit()
    return jsonify({'message': 'Supplier deleted successfully'})