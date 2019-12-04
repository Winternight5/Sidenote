from datetime import datetime
from . import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import backref
    
class User(UserMixin, db.Model):
"""
This class establishes a user. Tracks things like email, id, password and posts.
"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    settings = db.Column(db.Text, default='day')
    tags = db.Column(db.Text)
    post = db.relationship('Post', backref='user', lazy='dynamic')
    relations = db.relationship('Post', secondary="share", backref=backref('shareto', lazy='dynamic'))

    def set_password(self, password):
"""Generates password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
"""Makes sure password is valid"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
"""How a User object would print out"""
        return '<User {}>'.format(self.email)


class Post(db.Model):
"""
This class establishes a post object. This is shared with user class.
"""
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    imgUrl = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    readAllowed = db.Column(db.Boolean)  # don't need this
    writeAllowed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
"""Prints the post"""
        return '<Posts {}>'.format(self.body)

class Share(db.Model):
"""Enables sharing by using user and post class"""
    __tablename__ = "share"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)

    def __repr__(self):
"""How a shared post would print out"""
        return '<Share {}>'.format(self.post_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
