from flask import Blueprint

bp = Blueprint('quiz', __name__)

from src.quiz import routes  # cyclic import prevention
