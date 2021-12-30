"""
A module which creates a blueprint of 'posts' application.
"""

from flask import Blueprint

bp = Blueprint('posts', __name__)

from src.posts import routes  # cyclic import prevention
