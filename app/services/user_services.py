from app.models.user import User
from app import db

def create_user(username, email ,password):
    try:
        novo_usuario = User(username=username, email=email, password=password)
        db.session.add(novo_usuario)
        db.session.commit()
        return novo_usuario
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao criar usuario: {e}")
        return None

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


