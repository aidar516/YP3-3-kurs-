from flask import Blueprint, request, jsonify
from models import db, Genre

genre_bp = Blueprint('genre', __name__)

@genre_bp.route('/', methods=['GET'])
def get_genres():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'genre_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search')

    query = Genre.query.filter_by(is_deleted=False)

    if search:
        query = query.filter(Genre.genre_name.contains(search))

    if order == 'asc':
        query = query.order_by(getattr(Genre, sort_by).asc())
    else:
        query = query.order_by(getattr(Genre, sort_by).desc())

    genres = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'genres': [genre.serialize() for genre in genres.items],
        'total': genres.total,
        'pages': genres.pages,
        'current_page': genres.page
    })

@genre_bp.route('/<int:genre_id>', methods=['GET'])
def get_genre(genre_id):
    genre = Genre.query.filter_by(genre_id=genre_id, is_deleted=False).first()
    if not genre:
        return jsonify({'message': 'Genre not found'}), 404

    return jsonify(genre.serialize())

@genre_bp.route('/', methods=['POST'])
def create_genre():
    data = request.get_json()
    if not data or not 'genre_name' in data:
        return jsonify({'message': 'Missing parameters'}), 400

    new_genre = Genre(
        genre_name=data['genre_name'],
        description=data.get('description')
    )

    db.session.add(new_genre)
    db.session.commit()

    return jsonify({'message': 'Genre created successfully', 'genre_id': new_genre.genre_id}), 201

@genre_bp.route('/<int:genre_id>', methods=['PUT'])
def update_genre(genre_id):
    genre = Genre.query.filter_by(genre_id=genre_id, is_deleted=False).first()
    if not genre:
        return jsonify({'message': 'Genre not found'}), 404

    data = request.get_json()
    genre.genre_name = data.get('genre_name', genre.genre_name)
    genre.description = data.get('description', genre.description)

    db.session.commit()
    return jsonify({'message': 'Genre updated successfully'})

@genre_bp.route('/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    genre = Genre.query.filter_by(genre_id=genre_id, is_deleted=False).first()
    if not genre:
        return jsonify({'message': 'Genre not found'}), 404

    genre.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Genre deleted successfully'})

@genre_bp.route('/restore', methods=['POST'])
def restore_genres():
    data = request.get_json()
    genre_ids = data.get('genre_ids')
    if not genre_ids:
        return jsonify({'message': 'No genre IDs provided'}), 400

    genres = Genre.query.filter(Genre.genre_id.in_(genre_ids), Genre.is_deleted == True).all()
    for genre in genres:
        genre.is_deleted = False

    db.session.commit()
    return jsonify({'message': f'Restored {len(genres)} genres'})