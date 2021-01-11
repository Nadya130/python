from app import app, db
from models import User
from requests.auth import HTTPBasicAuth

db.create_all()
test_app = app.test_client()

user = {'username': 'test_name', 'password': '123', 'email': 'test@mail.com'}
name = 'test_name'
password = '123'
put_user = {'username': 'new name', 'password': 'new pass', 'email': 'test@mail.com'}


def login(user):
    return test_app.get('/user/login', json=user).json.get('token')


def get_id():
    return User.query.filter_by(username=name).first().id


def get_id_2():
    return User.query.filter_by(username='new name').first().id


def test_create_user():
    data = test_app.post('/user', json=user)
    assert '200' in str(data)


def test_bad_create_user():
    data = test_app.post('/user', json={'username': name, 'email': 'test@mail.com'})
    assert '204' in str(data)


def test_login():
    data = test_app.get('/user/login', json=user)
    assert '200' in str(data)


def test_bad_login():
    data = test_app.get('/user/login', json={'foo': 'bar'})
    assert '401' in str(data)


def test_logout():
    data = test_app.get('/user/logout')
    print(data)
    assert '200' in str(data)


def test_get_userId():
    data = test_app.get('/user/' + str(get_id()), headers={'x-access-token': str(login(user))})
    assert '200' in str(data)


def test_put_userId():
    data = test_app.put('/user/' + str(get_id()), json=({'username': 'new name', 'password': 'new pass'}),
                        headers={'x-access-token': str(login(user))})
    assert '202' in str(data)


def test_get_all_users():
    data = test_app.get('/users', headers={'x-access-token': str(login(put_user))})
    assert '200' in str(data)

def test_bad_userId():
    data = test_app.delete('/user/99999999', headers={'x-access-token': str(login(put_user))})
    assert '404' in str(data)


def test_delete_userId():
    data = test_app.delete('/user/' + str(get_id_2()), headers={'x-access-token': str(login(put_user))})
    assert '201' in str(data)
