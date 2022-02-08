"""
The module renders backend view-functions' behavior
of the BP-registered application "quiz"
during client-server interaction through HTML templates.
"""

from flask import current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
#
from src.main.service import session_create
from src.quiz import bp
from src.quiz.models import Result, Test, Question
from src.quiz.forms import OptionMultiForm


@bp.route("/tests/")
@login_required
def tests_list_page():
    """
    The function manages tests display procedure.

    :return str: an HTML template for tests (list) page
    """
    tests = Test.query.order_by(Test.id).paginate(
        per_page=current_app.config['TABLES_PER_PAGE']
    )
    return render_template("quiz/tests.html", tests=tests)


@bp.route("/tests/<uuid:test_uuid>", methods=["GET", "POST"])
@login_required
def test_view_page(test_uuid):
    """
    The function manages the display of details about a test.

    :param UUID test_uuid: the UUID of an instance of "Test" ORM model
    :return str: an HTML template for test details page
    """
    test = Test.query.filter_by(uuid=test_uuid).first()
    return render_template("quiz/test_details.html", test=test)


@bp.route("/tests/<uuid:test_uuid>/results/", methods=["POST"])
@login_required
def result_create_view(test_uuid):
    """
    The function manages test result creation procedure.

    :param UUID test_uuid: the UUID of an instance of "Test" ORM model
    :return str: an HTML template for result update (test proceed) page
    """
    result = Result(
        user_id=current_user.id,
        test_id=Test.query.filter_by(uuid=test_uuid).first().id,
    )
    session_create(result)
    return redirect(url_for("quiz.result_update_question_view_page",
                            test_uuid=test_uuid,
                            result_uuid=result.uuid
                            )
                    )


@bp.route("/tests/<uuid:test_uuid>/results/<uuid:result_uuid>/questions/", methods=["GET", "POST"])
@login_required
def result_update_question_view_page(test_uuid, result_uuid):
    """
    The function manages test proceeding (result update) procedure.

    :param UUID test_uuid: the UUID of an instance of "Test" ORM model
    :param UUID result_uuid: the UUID of an instance of "Result" ORM model
    :return str: an HTML template for result update page/result view page
    """
    result = Result.query.filter_by(uuid=result_uuid).first()
    last_question = result.last_question
    question = Question.query.filter_by(
        test_id=Test.query.filter_by(uuid=test_uuid).first().id,
        order_number=last_question + 1
    ).first()
    form = OptionMultiForm()
    options = question.options
    form.options.choices = [option.text for option in options]
    if form.validate_on_submit():
        answer = request.form.get('options')
        model_option = list(filter(lambda option: option.text == answer, options))[0]
        result = Result.query.filter_by(uuid=result_uuid).first()
        result.update_result(model_option)
        if result.state == Result.State.FINISHED:
            return redirect(url_for("quiz.result_view_page",
                                    test_uuid=test_uuid,
                                    result_uuid=result_uuid)
                            )
        else:
            return redirect(url_for("quiz.result_update_question_view_page",
                                    test_uuid=test_uuid,
                                    result_uuid=result.uuid
                                    )
                            )
    return render_template("quiz/questions.html", form=form, question=question)


@bp.route("/tests/<uuid:test_uuid>/results/<uuid:result_uuid>/details")
@login_required
def result_view_page(test_uuid, result_uuid):
    """
    The function manages result display procedure.

    :param UUID test_uuid: the UUID of an instance of "Test" ORM model
    :param UUID result_uuid: the UUID of an instance of "Result" ORM model
    :return str: an HTML template for result view page
    """
    result = Result.query.filter_by(uuid=result_uuid).first()
    test = Test.query.filter_by(uuid=test_uuid).first()
    return render_template("quiz/result_details.html",
                           result=result,
                           test=test)
