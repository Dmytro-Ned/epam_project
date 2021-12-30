"""
A module which creates a blueprint of 'main' application.
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from src.main import routes  # cyclic import prevention
