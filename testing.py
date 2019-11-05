import pytest
from app.models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required

from app import app


@pytest.fixture(scope='module')
def new_user():
    user = User(email='patkennedy79@gmail.com', firstname='firstname',
                lastname='lastname', password_hash=generate_password_hash('1234'))
    return user


@pytest.fixture(scope='module')
def new_note():
    note = Post(body='blah blah blah', user_id='1')
    return note


def test_new_user(new_user):
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password_hash != generate_password_hash('1234')


def test_login(new_user):
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.check_password('1234') == True

    # print(app.post('/login'))
    #assert login_user(new_user)
    assert new_user.is_authenticated == True


def test_logout(new_user):
    assert new_user.is_authenticated == True
    #assert logout_user()


def test_new_note(new_note):
    assert new_note.body != None
