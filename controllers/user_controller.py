from app import app, db
from models import *
from flask import request, jsonify, make_response
from flask import json
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if username and password and email:
        new_user = User(username=username, email=email, password=password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(status='created'), 200
    else:
        return jsonify(status='Bad data'), 204


@app.route('/user/<id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def userId(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function as you are not admin'})
    user = User.query.filter_by(id=id).first()
    if user is None:
        return jsonify(status='not found user'), 404

    if request.method == 'GET':
        return jsonify(status='User exist', username=user.username, email=user.email, admin=user.admin), 200

    if request.method == 'PUT':
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        email = request.json.get('email', None)
        admin = request.json.get('admin', None)
        if username or password or email or admin:
            user.username = username
            user.email = email
            user.password = generate_password_hash(password)
            user.admin = admin
            db.session.commit()
            return jsonify(status='updated', name=user.username, email=user.email, admin=user.admin), 202
        else:
            return jsonify(status='Bad data'), 204

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify(status='deleted', name=user.username), 201


@app.route('/user/login', methods=['GET'])
def login_user():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/user/logout', methods=['GET'])
def logout_user():
    return jsonify({"Logout success"}), 200


@app.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function as you are not admin'})
    users = User.query.all()
    users_list = {'users_list': []}
    for user in users:
        users_list['users_list'].append(
            {'id': user.id, 'username': user.username, 'email': user.email, 'admin': user.admin})
    return jsonify(users_list)
