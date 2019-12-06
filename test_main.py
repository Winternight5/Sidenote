# import pytest
# from app import routes, events
# from app.models import User, Post
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import current_user, login_user, logout_user


# @pytest.fixture(scope='module')
# def new_user():
#     """
#     This file contatins all the testing for Travis CI.
#     To run locally use command:
#     $ pytest
#     """
#     user = User(email='patkennedy79@gmail.com', firstname='firstname',
#                 lastname='lastname', password_hash=generate_password_hash('1234'), settings='dark')
#     return user


# @pytest.fixture(scope='module')
# def new_note():
#     note = Post(body='blah blah blah', user_id='1', writeAllowed=False)
#     return note

# # Pytest 1
# # Test validating of new user patkennedy79@gmail.com
# def test_new_user(new_user):
#     assert new_user.email == 'patkennedy79@gmail.com'
#     assert new_user.password_hash != generate_password_hash('1234')

# # Pytest 2
# # Test authentication of new user
# def test_login(new_user):
#     assert new_user.is_authenticated == True

# # Pytest 3
# # Test changing user's theme
# def test_changetheme(new_user):
#     assert new_user.settings == 'dark'

# # Pytest 4
# # Test note's model
# def test_new_note(new_note):
#     assert new_note.body != None


# # Pytest 5
# # Test writing authorization
# def test_noteWriteAccess(new_note):
#     assert new_note.writeAllowed == False
    
# # Pytest 6
# # Test concat of string List items into single Sting
# def test_listToString():
#     list = ['this', 'is', 'a', 'string']
#     assert routes.listToString(list) == 'this is a string'
    
# # Pytest 7
# # Test note Data
# def test_noteData():
#     title = 'New Note'
#     bgcolor = 'yellow'
#     icon = 'event_note'
#     tags = 'Test'
#     body = 'This is a Test'
#     canvas = False
    
#     result = {
#         'title': '' if title is None else title,
#         'icon': icon,
#         'note_bgcolor': '' if bgcolor is None else bgcolor,
#         'tags': '' if tags is None else tags,
#         'body': '' if body is None else body
#     }
    
#     assert routes.noteData(title, bgcolor, tags, body, canvas) == result
    
# # Pytest 8
# # Test concat of string List items into single Sting
# #def test_newList():=
#     #assert events.clearDatas(currentRoom) == datas[currentRoom]
