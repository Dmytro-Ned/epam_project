from flask import render_template
#
from src.errors import bp


@bp.app_errorhandler(403)
def error_403(error):
    return render_template("errors/error_403.html"), 403  # flask route returns HTTP status code as 2nd value


@bp.app_errorhandler(404)
def error_404(error):
    return render_template("errors/error_404.html"), 404


@bp.app_errorhandler(500)
def error_500(error):
    return render_template("errors/error_500.html"), 500
