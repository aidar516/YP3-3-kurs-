from flask import Blueprint, jsonify, request
from models import *

publisher_bp = Blueprint('publisher', __name__)

@publisher_bp.route('/', methods=['GET'])
def get_publishers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'publisher_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search')

    query = Publisher.query.filter_by(is_deleted=False)

    if search:
        query = query.filter(Publisher.publisher_name.contains(search))

    if order == 'asc':
        query = query.order_by(getattr(Publisher, sort_by).asc())
    else:
        query = query.order_by(getattr(Publisher, sort_by).desc())

    publishers = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'publishers': [publisher.serialize() for publisher in publishers.items],
        'total': publishers.total,
        'pages': publishers.pages,
        'current_page': publishers.page
    })

@publisher_bp.route('/<int:publisher_id>', methods=['GET'])
def get_publisher(publisher_id):
    publisher = Publisher.query.filter_by(publisher_id=publisher_id, is_deleted=False).first()
    if not publisher:
        return jsonify({'message': 'Publisher not found'}), 404

    return jsonify(publisher.serialize())

@publisher_bp.route('/', methods=['POST'])
def create_publisher():
    data = request.get_json()
    if not data or not all(key in data for key in ['publisher_name', 'address', 'phone']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_publisher = Publisher(
        publisher_name=data['publisher_name'],
        address=data['address'],
        phone=data['phone'],
        website=data.get('website')
    )

    db.session.add(new_publisher)
    db.session.commit()

    return jsonify({'message': 'Publisher created successfully', 'publisher_id': new_publisher.publisher_id}), 201

@publisher_bp.route('/<int:publisher_id>', methods=['PUT'])
def update_publisher(publisher_id):
    publisher = Publisher.query.filter_by(publisher_id=publisher_id, is_deleted=False).first()
    if not publisher:
        return jsonify({'message': 'Publisher not found'}), 404

    data = request.get_json()
    publisher.publisher_name = data.get('publisher_name', publisher.publisher_name)
    publisher.address = data.get('address', publisher.address)
    publisher.phone = data.get('phone', publisher.phone)
    publisher.website = data.get('website', publisher.website)

    db.session.commit()
    return jsonify({'message': 'Publisher updated successfully'})

@publisher_bp.route('/<int:publisher_id>', methods=['DELETE'])
def delete_publisher(publisher_id):
    publisher = Publisher.query.filter_by(publisher_id=publisher_id, is_deleted=False).first()
    if not publisher:
        return jsonify({'message': 'Publisher not found'}), 404

    publisher.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Publisher deleted successfully'})

@publisher_bp.route('/restore', methods=['POST'])
def restore_publishers():
    data = request.get_json()
    publisher_ids = data.get('publisher_ids')
    if not publisher_ids:
        return jsonify({'message': 'No publisher IDs provided'}), 400

    publishers = Publisher.query.filter(Publisher.publisher_id.in_(publisher_ids), Publisher.is_deleted == True).all()
    for publisher in publishers:
        publisher.is_deleted = False

    db.session.commit()
    return jsonify({'message': f'Restored {len(publishers)} publishers'})