from app.models.user import User
from app import db

def create_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()
