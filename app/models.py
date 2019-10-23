from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__  = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    settings = db.Column(db.Text)
    tags = db.Column(db.Text)
    post = db.relationship('Post', backref='user', lazy='dynamic') 
    share = db.relationship('AllPosts', backref='user', lazy='dynamic') 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)    

class Post(db.Model):
    __tablename__  = "post"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    imgUrl = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    readAllowed = db.Column(db.Boolean)
    writeAllowed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    share = db.relationship('AllPosts', backref='post', lazy='dynamic') 
    # share to another (multiple) user at a later time
    # share_id = db.Column(db.text)

    def __repr__(self):
        return '<Posts {}>'.format(self.body)
        
class AllPosts(db.Model):
    __tablename__ = 'allposts'
    id = db.Column(db.Integer, primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True)
    
    #https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query
'''class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Tags {}>'.format(self.body)
        
class tagPostsRelations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag = db.relationship('Tag', backref='tagPostsRelations', lazy='dynamic')

    def __repr__(self):
        return '<tagPostsRelations {}>'.format(self.body) '''
#https://stackoverflow.com/questions/24799753/database-design-for-apps-using-hashtags/24800716
#https://www.quora.com/How-does-Twitter-implement-hashtags-I%E2%80%99m-looking-for-details-on-technology-stack-high-level-database-schema-and-scalability-limitations

@login.user_loader
def load_user(id):
    return User.query.get(int(id))