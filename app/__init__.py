import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask.logging import default_handler

mail = Mail()
jwt_manager = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cors = CORS()


def create_app(config_class="config.DevelopmentConfig"):
    """this function creates and configure the flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)

    return app


def register_blueprints(app):
    from app.users import users_bp
    from app.journals import journals_bp
    from app.categories import category_bp

    app.register_blueprint(users_bp, url_prefix="/api/auth")
    app.register_blueprint(journals_bp, url_prefix="/api/journal-entries")
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    return


def initialize_extensions(app):
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app)


def configure_logging(app):
    if app.config["LOG_TO_STDOUT"]:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        app.logger.removeHandler(default_handler)
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=16384, backupCount=3
        )

        file_handler.setLevel(logging.INFO)
        logs_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(module)s %(filename)s: %(lineno)d]"
        )
        file_handler.setFormatter(logs_formatter)

        app.logger.handlers.clear()
        app.logger.addHandler(file_handler)

        return


@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from app.models import User  # type: ignore

    identity = jwt_data["sub"]
    user_id = identity["_id"]
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None

    return user


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.get(user_id)
