from flask import Blueprint

bp = Blueprint('err', __name__)

from src.errors import handlers  # circular import prevention
