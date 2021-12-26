from flask import Blueprint

bp = Blueprint('main', __name__)

from src.main import routes  # cyclic import prevention
