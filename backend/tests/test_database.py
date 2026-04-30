from database import get_user, create_user, delete_user
from argon2 import PasswordHasher



def test_create_user():
    ph = PasswordHasher()
    create_user('usertest', 'usertest@gmail.com', 'usertest', ph.hash('password'), 'user')
    user = get_user('usertest')
    assert user['username'] == 'usertest'
    assert user['email'] == 'usertest@gmail.com'

def test_get_user():
    user = get_user('usertest')
    assert user['username'] == 'usertest'
    assert user['email'] == 'usertest@gmail.com'


def test_delete_user():
    delete_user('usertest')
    user = get_user('usertest')
    assert user is None

