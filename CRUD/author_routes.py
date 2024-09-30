from flask import Blueprint, request, jsonify
from models import db, Author

author_bp = Blueprint('author', __name__)

@author_bp.route('/', methods=['GET'])
def get_authors():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'author_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search')

    query = Author.query.filter_by(is_deleted=False)

    if search:
        query = query.filter(Author.author_name.contains(search) | Author.author_surname.contains(search))

    if order == 'asc':
        query = query.order_by(getattr(Author, sort_by).asc())
    else:
        query = query.order_by(getattr(Author, sort_by).desc())

    authors = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'authors': [author.serialize() for author in authors.items],
        'total': authors.total,
        'pages': authors.pages,
        'current_page': authors.page
    })

@author_bp.route('/<int:author_id>', methods=['GET'])
def get_author(author_id):
    author = Author.query.filter_by(author_id=author_id, is_deleted=False).first()
    if not author:
        return jsonify({'message': 'Author not found'}), 404

    return jsonify(author.serialize())

@author_bp.route('/', methods=['POST'])
def create_author():
    data = request.get_json()
    if not data or not 'author_name' in data:
        return jsonify({'message': 'Missing parameters'}), 400

    new_author = Author(
        author_name=data['author_name'],
        author_surname=data.get('author_surname'),
        biography=data.get('biography')
    )

    db.session.add(new_author)
    db.session.commit()

    return jsonify({'message': 'Author created successfully', 'author_id': new_author.author_id}), 201

@author_bp.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    author = Author.query.filter_by(author_id=author_id, is_deleted=False).first()
    if not author:
        return jsonify({'message': 'Author not found'}), 404

    data = request.get_json()
    author.author_name = data.get('author_name', author.author_name)
    author.author_surname = data.get('author_surname', author.author_surname)
    author.biography = data.get('biography', author.biography)

    db.session.commit()
    return jsonify({'message': 'Author updated successfully'})

@author_bp.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.filter_by(author_id=author_id, is_deleted=False).first()
    if not author:
        return jsonify({'message': 'Author not found'}), 404

    author.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Author deleted successfully'})

@author_bp.route('/restore', methods=['POST'])
def restore_authors():
    data = request.get_json()
    author_ids = data.get('author_ids')
    if not author_ids:
        return jsonify({'message': 'No author IDs provided'}), 400

    authors = Author.query.filter(Author.author_id.in_(author_ids), Author.is_deleted == True).all()
    for author in authors:
        author.is_deleted = False

    db.session.commit()
    return jsonify({'message': f'Restored {len(authors)} authors'})