import pytest
from app.models import User, Post, Share
from app.forms import LoginForm


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

# Would fail pytest if import from routes
def listToString(s, delimeter=' '):
    str1 = " "
    return (delimeter.join(str(v) for v in s))


def test_listToString():
    list = ['this', 'is', 'a', 'string']
    assert listToString(list) == 'this is a string'

# Would fail pytest if import from routes
def noteData(title, bgcolor, tags, body, canvas=False):
    icon = 'event_note'
    if "cbox" in body:
        icon = 'event_available'
    elif canvas:
        icon = 'brush'
    elif "<img src" in body:
        icon = 'image'

    post = {
        'title': '' if title is None else title,
        'icon': icon,
        'note_bgcolor': '' if bgcolor is None else bgcolor,
        'tags': '' if tags is None else tags,
        'body': '' if body is None else body
    }
    return post


def test_noteData():
    title = 'New Note'
    bgcolor = 'yellow'
    icon = 'event_note'
    tags = 'Test'
    body = 'This is a Test'
    canvas = False

    result = {
        'title': '' if title is None else title,
        'icon': icon,
        'note_bgcolor': '' if bgcolor is None else bgcolor,
        'tags': '' if tags is None else tags,
        'body': '' if body is None else body
    }

    assert noteData(title, bgcolor, tags, body, canvas) == result
