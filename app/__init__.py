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
    from app.models.produto import Produto
    from app.models.persona import Persona
    from app.models.epico import Epico
    from app.models.historia_usuario import HistoriaUsuario
    from app.models.requisito import Requisito
    from app.models.backlog import Backlog
    from app.models.revisao import Revisao

    login_manager.init_app(app)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.produto import produto_bp
    from .routes.backlog import backlog_bp
    from .routes.gpt import gpt_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(backlog_bp)
    app.register_blueprint(gpt_bp)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
