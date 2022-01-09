"""
A module which creates a blueprint of 'errors' application.
"""

from flask import Blueprint

bp = Blueprint('err', __name__)  # pylint: disable=C0103

from src.errors import handlers  # circular import prevention
