"""
A module which creates a blueprint of 'main' application.
"""

from flask import Blueprint

bp = Blueprint('main', __name__)  # pylint: disable=C0103

from src.main import routes  # cyclic import prevention
