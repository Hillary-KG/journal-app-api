import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS

mail = Mail()
jwt_manager = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class="config.DevelopmentConfig"):
    """this function creates and configure the flask app"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    initialize_extensions(app)
    register_blueprints(app)
    
    return app
    
    
    
    
def register_blueprints(app):
    pass

def initialize_extensions(app):
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager.init_app(app)
    login_manager.init_app(app)

def configure_login(app):
    pass

@jwt_manager.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from models import User  # type: ignore

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