from flask import render_template
#
from src.main import bp


@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("home_page.html")
