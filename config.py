import os
from datetime import datetime
from dotenv import load_dotenv


class Config:
    """This is the base Config class"""

    # define default configs
    TESTING = os.getenv("TESTING")
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY", default="")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = "Africa/Nairobi"
    SERVER_NAME = os.getenv("SERVER_NAME")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL")
    MAIL_PORT = os.getenv("MAIL_PORT")
    ADMINS = os.getenv("ADMINS")
    # MAIL_SUPPRESS_SEND = os.environ.get("MAIL_SUPPRESS_SEND")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

class DevelopmentConfig:
    """This class describes development environment config"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL_DEV", default="")
    
    
class ProductionConfig(Config):
    """This class describes the application config in production environment"""
    TESTING = True
    DEBUG = True
    
    
    
config = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}