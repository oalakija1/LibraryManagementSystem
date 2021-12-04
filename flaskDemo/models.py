from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"




class Books(db.Model):
    __table__ = db.Model.metadata.tables['books']

class Inventory(db.Model):
    __table__ = db.Model.metadata.tables['inventory']

class Borrower_Copies(db.Model):
    __table__ = db.Model.metadata.tables['borrower_copies']

class Borrower(db.Model):
    __table__ = db.Model.metadata.tables['borrower']
