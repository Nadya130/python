from app import app, db
from models import *
from flask import request, jsonify, json
from functools import wraps
import jwt


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


@app.route('/credit/<id>', methods=['DELETE'])
@token_required
def delete_credit(current_user, id):
    credit = Credit.query.filter_by(id=id, userId=current_user.id).first()
    try:
        db.session.delete(credit)
        db.session.commit()
        return jsonify(status='deleted'), 201
    except:
        return jsonify(status='credit not found for this user'), 404


@app.route('/credit/<id>', methods=['GET'])
@token_required
def get_credit_by_id(current_user, id):

    credit = Credit.query.filter_by(id=id, userId=current_user.id).first()

    if credit is None:
        return jsonify(status='credit not found for this user'), 404
    return jsonify(credit={'id': credit.id, 'sum': credit.sum}), 200


@app.route('/credit', methods=['POST'])
@token_required
def create_credit(current_user):
    sum = request.json.get('sum', None)
    status = request.json.get('status', None)
    bankId = request.json.get('bankId', None)

    if sum and status and bankId:
        new_credit = Credit(sum=sum, status=status, userId=current_user.id, bankId=bankId)
        db.session.add(new_credit)
        db.session.commit()

        return jsonify(status='created'), 200
    else:
        return jsonify(status='Bad data'), 204


@app.route('/credit/<id>', methods=['PUT'])
@token_required
def creditId(current_user, id):
    credit = Credit.query.filter_by(id=id, userId=current_user.id).first()
    if credit is None or credit.userId != current_user.id:
        return jsonify(status='not found credit'), 404
    if request.method == 'PUT':
        sum = request.json.get('sum', None)
        status = request.json.get('status', None)
        bankId = request.json.get('bankId', None)
        if sum and status and bankId:
            credit.sum = sum
            credit.status = status
            credit.bankId = bankId
            db.session.commit()

            return jsonify(status='updated'), 202
        else:
            return jsonify(status='Bad data'), 204


@app.route('/credits', methods=['GET'])
@token_required
def get_all_credits(current_user):
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function as you are not admin'})
    credits = Credit.query.all()
    credits_list = {'credits_list': []}
    for credit in credits:
        credits_list['credits_list'].append(
            {'id': credit.id, 'sum': credit.sum, 'userId': credit.userId, 'bankId': credit.bankId})
    return jsonify(credits_list)
