from flask import Blueprint, jsonify, request
from models import *

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'user_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search')

    query = User.query.filter_by(is_deleted=False)

    if search:
        query = query.filter(User.user_name.contains(search) | User.user_surname.contains(search))

    if order == 'asc':
        query = query.order_by(getattr(User, sort_by).asc())
    else:
        query = query.order_by(getattr(User, sort_by).desc())

    users = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'users': [user.serialize() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': users.page
    })


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user.serialize())


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.user_name = data.get('user_name', user.user_name)
    user.user_surname = data.get('user_surname', user.user_surname)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(user_id=user_id, is_deleted=False).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@user_bp.route('/restore', methods=['POST'])
def restore_users():
    data = request.get_json()
    user_ids = data.get('user_ids')
    if not user_ids:
        return jsonify({'message': 'No user IDs provided'}), 400

    users = User.query.filter(User.user_id.in_(user_ids), User.is_deleted == True).all()
    for user in users:
        user.is_deleted = False

    db.session.commit()
    return jsonify({'message': f'Restored {len(users)} users'})