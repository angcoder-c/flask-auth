from enum import unique
from flask import current_app, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager, db

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique = True)
    email = db.Column(db.String(256), nullable = False, unique = True)
    profile_picture = db.Column(db.String)
    cover_photo = db.Column(db.String)
    password = db.Column(db.String(128), nullable = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))