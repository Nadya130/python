from app import app, db
from models import *
from requests.auth import HTTPBasicAuth

db.create_all()
test_app = app.test_client()

user = {'username': 'test_name', 'password': '123', 'email': 'test@mail.com'}
name = 'test_name'
password = '123'

credit = {'sum': '4000', 'status': 'norm', 'bankId': '1'}
bank = Bank(name='Avowal', budget=517000)
db.session.add(bank)
db.session.commit()


def login():
    return test_app.get('/user/login', json=user).json.get('token')


def get_credit():
    return Credit.query.all()[0].id


def get_id():
    return User.query.filter_by(username=name).first().id


def test_start():
    test_app.post('/user', json=user)


def test_get_all_credits():
    data = test_app.get('/credits', headers={'x-access-token': str(login())})
    assert '200' in str(data)


def test_create_credit():
    data = test_app.post('/credit', json=credit, headers={'x-access-token': str(login())})
    assert '200' in str(data)


def test_get_credit_by_id():
    data = test_app.get('/credit/' + str(get_credit()), headers={'x-access-token': str(login())})
    print(get_credit())
    assert '200' in str(data)


def test_bad_get_credit_by_id():
    data = test_app.get('/credit/9999999', headers={'x-access-token': str(login())})
    print(get_credit())
    assert '404' in str(data)


def test_put_credit():
    data = test_app.put('/credit/' + str(get_credit()), json=credit, headers={'x-access-token': str(login())})
    assert '202' in str(data)


def test_bad_put_credit():
    data = test_app.put('/credit/99999', json=credit, headers={'x-access-token': str(login())})
    assert '404' in str(data)


def test_bad_put_credit_no_login():
    data = test_app.put('/credit/99999', json=credit, headers={'x-access-token': '23213'})
    assert '401' in str(data)


def test_delete_credit():
    data = test_app.delete('/credit/' + str(get_credit()), headers={'x-access-token': str(login())})
    assert '201' in str(data)


def test_end():
    test_app.delete('/user/' + str(get_id()), headers={'x-access-token': str(login())})
