from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

    db.init_app(app)

    from app.models import user

    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
