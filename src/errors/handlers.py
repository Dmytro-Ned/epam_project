"""
The module handles custom HTML Error templates.
"""

from flask import render_template
#
from src.errors import bp


@bp.app_errorhandler(403)
def error_403(error):  # pylint: disable=W0613
    """
    Manages rendering of custom error templates
    on errors with status code 403.

    :param error: an occurring error
    :return str: a custom HTML template
    """
    return render_template("errors/error_403.html"), 403  # HTTP status code as the 2nd value


@bp.app_errorhandler(404)
def error_404(error):  # pylint: disable=W0613
    """
    Manages rendering of custom error templates
    on errors with status code 404.

    :param error: an occurring error
    :return str: a custom HTML template
    """
    return render_template("errors/error_404.html"), 404


@bp.app_errorhandler(500)
def error_500(error):  # pylint: disable=W0613
    """
    Manages rendering of custom error templates
    on errors with status code 500.

    :param error: an occurring error
    :return str: a custom HTML template
    """
    return render_template("errors/error_500.html"), 500
