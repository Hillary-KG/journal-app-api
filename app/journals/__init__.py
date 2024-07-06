from flask import Blueprint

journals_bp = Blueprint("journals_bp", __name__)

from . import views