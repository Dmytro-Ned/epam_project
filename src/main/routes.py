from flask import escape, render_template
#
from src.main import bp


@bp.route("/")
@bp.route("/home")
def home_page():
    return render_template("home_page.html")


@bp.route("/gr_<string:var>")
def greet_var(var):
    return f"Hello, {escape(var)}"


@bp.route("/real")
def real_template():  # TODO: remove
    return render_template("real.html")
