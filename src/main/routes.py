"""
The module renders backend view-functions' behavior
of the BP-registered application "main"
during client-server interaction through HTML templates.
"""

from flask import render_template
#
from src.main import bp


@bp.route("/")
@bp.route("/home")
def home_page():
    """
    The function manages rendering
    of the main page of the site.

    :return str: an HTML template for home page
    """
    return render_template("home_page.html")
