from flask import Blueprint

category_bp = Blueprint("category_bp", __name__)

from . import view