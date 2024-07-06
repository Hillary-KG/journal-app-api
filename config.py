import os
from datetime import datetime
from dotenv import load_dotenv


class Config:
    """This is the base Config class"""

    # define default configs
    TESTING = os.getenv("TESTING")
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TIMEZONE = "Africa/Nairobi"
    SERVER_NAME = os.getenv("SERVER_NAME")
    LOG_TO_STDOUT = os.getenv("LOG_TO_STDOUT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
    MAIL_PORT = os.getenv("MAIL_PORT")
    ADMINS = os.getenv("ADMINS")
    # MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

class DevelopmentConfig(Config):
    """This class describes development environment config"""
    TESTING = True
    DEBUG = True
    LOG_TO_STDOUT = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL_DEV")
    
    
class ProductionConfig(Config):
    """This class describes the application config in production environment"""
    TESTING = True
    DEBUG = True
    
    
    
config = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}