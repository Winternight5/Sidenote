import pytest
from app.models import User, Post, Share
from app.forms import LoginForm

# form = LoginForm()


def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_add_user_to_db(db):
    test_user = User(email='test_user@gmail.com', firstname='test',
                     lastname='user', password_hash='1234', settings='dark')
    db.session.add(test_user)
    db.session.commit()
    assert len(User.query.all()) == 1


def test_verfy_user_exists(db):
    user = User.query.get(1)
    assert user.is_authenticated == True


def test_theme(db):
    assert User.query.get(1).settings == 'dark'


def test_new_note(db):
    note = Post(body='blah blah blah', user_id='1', writeAllowed=False)
    db.session.add(note)
    db.session.commit()
    assert Post.query.get(1).body == 'blah blah blah'


def test_valid_register(client, db):
    response = client.post('/login',
                           data=dict(firstname='testing', email='testing@testing.com',
                                     password='testing', confirm='testing'),
                           follow_redirects=True)
    assert response.status_code == 200
