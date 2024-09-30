from flask import Blueprint, jsonify, request
from models import *

role_bp = Blueprint('role', __name__)

@role_bp.route('/', methods=['GET'])
def get_roles():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'role_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search')

    query = Role.query

    if search:
        query = query.filter(Role.role_name.contains(search))

    if order == 'asc':
        query = query.order_by(getattr(Role, sort_by).asc())
    else:
        query = query.order_by(getattr(Role, sort_by).desc())

    roles = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'roles': [role.serialize() for role in roles.items],
        'total': roles.total,
        'pages': roles.pages,
        'current_page': roles.page
    })

@role_bp.route('/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    return jsonify(role.serialize())

@role_bp.route('/', methods=['POST'])
def create_role():
    data = request.get_json()
    if not data or not 'role_name' in data:
        return jsonify({'message': 'Missing parameters'}), 400

    new_role = Role(role_name=data['role_name'])

    db.session.add(new_role)
    db.session.commit()

    return jsonify({'message': 'Role created successfully', 'role_id': new_role.role_id}), 201

@role_bp.route('/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    data = request.get_json()
    role.role_name = data.get('role_name', role.role_name)

    db.session.commit()
    return jsonify({'message': 'Role updated successfully'})

@role_bp.route('/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = Role.query.filter_by(role_id=role_id).first()
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    db.session.delete(role)
    db.session.commit()
    return jsonify({'message': 'Role deleted successfully'})