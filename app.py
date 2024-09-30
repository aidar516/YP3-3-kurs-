from flask import Flask, redirect, jsonify, request, render_template, session, url_for
from config import Config
from flask_migrate import Migrate
from CRUD import crud_bp
from models import *
from admin import *

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
admin.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user and user.role.role_name == 'Администратор':
            return redirect('/admin')
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        if not data or not all(key in data for key in ['email', 'password']):
            return jsonify({'message': 'Missing parameters'}),


        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid email or password'}), 401

        user.generate_token()
        session['user_id'] = user.user_id

        if user.role.role_name == 'Администратор':
            return redirect('/admin')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register_user():
    data = request.form
    if not data or not all(key in data for key in ['first_name', 'last_name', 'email', 'password']):
        return jsonify({'message': 'Missing parameters'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400

    client_role = Role.query.filter_by(role_name='Пользователь').first()
    if not client_role:
        return jsonify({'message': 'Role "Пользователь" does not exist'}), 500

    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        role_id=client_role.role_id,
    )
    new_user.set_password(data['password'])
    new_user.generate_token()

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id}), 201


@app.route('/signin', methods=['POST', 'GET'])
def login_user():
    data = request.form
    if not data or not all(key in data for key in ['email', 'password']):
        return jsonify({'message': 'Missing parameters'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    user.generate_token()
    db.session.commit()

    return jsonify({'message': 'Logged in successfully', 'token': user.token}), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)
