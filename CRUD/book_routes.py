from flask import Blueprint, request, jsonify
from models import db, Book

book_bp = Blueprint('book', __name__)

@book_bp.route('/', methods=['GET'])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'book_id')
    order = request.args.get('order', 'asc')
    search = request.args.get('search')

    query = Book.query.filter_by(is_deleted=False)

    if search:
        query = query.filter(Book.book_name.contains(search))

    if order == 'asc':
        query = query.order_by(getattr(Book, sort_by).asc())
    else:
        query = query.order_by(getattr(Book, sort_by).desc())

    books = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'books': [book.serialize() for book in books.items],
        'total': books.total,
        'pages': books.pages,
        'current_page': books.page
    })

@book_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.filter_by(book_id=book_id, is_deleted=False).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    return jsonify(book.serialize())

@book_bp.route('/', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data or not 'book_name' in data:
        return jsonify({'message': 'Missing parameters'}), 400

    new_book = Book(
        book_name=data['book_name'],
        author_id=data.get('author_id'),
        genre_id=data.get('genre_id'),
        publisher_id=data.get('publisher_id'),
        price=data.get('price'),
        year=data.get('year'),
        description=data.get('description'),
        image=data.get('image')
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify({'message': 'Book created successfully', 'book_id': new_book.book_id}), 201

@book_bp.route('/update/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.filter_by(book_id=book_id, is_deleted=False).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    data = request.get_json()
    book.book_name = data.get('book_name', book.book_name)
    book.author_id = data.get('author_id', book.author_id)
    book.genre_id = data.get('genre_id', book.genre_id)
    book.publisher_id = data.get('publisher_id', book.publisher_id)
    book.price = data.get('price', book.price)
    book.year = data.get('year', book.year)
    book.description = data.get('description', book.description)
    book.image = data.get('image', book.image)

    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@book_bp.route('/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id, is_deleted=False).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    book.is_deleted = True
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

@book_bp.route('/restore', methods=['POST'])
def restore_books():
    data = request.get_json()
    book_ids = data.get('book_ids')
    if not book_ids:
        return jsonify({'message': 'No book IDs provided'}), 400

    books = Book.query.filter(Book.book_id.in_(book_ids), Book.is_deleted == True).all()
    for book in books:
        book.is_deleted = False

    db.session.commit()
    return jsonify({'message': f'Restored {len(books)} books'})