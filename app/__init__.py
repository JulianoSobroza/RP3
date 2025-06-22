from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from config import Config

import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.models.user import User

    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
