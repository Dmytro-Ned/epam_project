"""
A module which creates a blueprint of 'auth' application.
"""

from flask import Blueprint

bp = Blueprint('auth', __name__)  # pylint: disable=C0103

from src.auth import routes  # cyclic import prevention
