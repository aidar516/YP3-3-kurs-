from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, Transaction

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'transaction_id')
    order = request.args.get('order', 'asc')

    query = Transaction.query

    if order == 'asc':
        query = query.order_by(getattr(Transaction, sort_by).asc())
    else:
        query = query.order_by(getattr(Transaction, sort_by).desc())

    transactions = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'transactions': [transaction.serialize() for transaction in transactions.items],
        'total': transactions.total,
        'pages': transactions.pages,
        'current_page': transactions.page
    })

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404

    return jsonify(transaction.serialize())

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not data or not all(key in data for key in ['order_id', 'transaction_amount', 'transaction_type']):
        return jsonify({'message': 'Missing parameters'}), 400

    new_transaction = Transaction(
        order_id=data['order_id'],
        transaction_amount=data['transaction_amount'],
        transaction_type=data['transaction_type'],
        transaction_date=data.get('transaction_date', datetime.utcnow())
    )

    db.session.add(new_transaction)
    db.session.commit()

    return jsonify({'message': 'Transaction created successfully', 'transaction_id': new_transaction.transaction_id}), 201

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404

    data = request.get_json()
    transaction.order_id = data.get('order_id', transaction.order_id)
    transaction.transaction_amount = data.get('transaction_amount', transaction.transaction_amount)
    transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
    transaction.transaction_date = data.get('transaction_date', transaction.transaction_date)

    db.session.commit()
    return jsonify({'message': 'Transaction updated successfully'})

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted successfully'})