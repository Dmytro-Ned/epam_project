"""
The module renders backend view-functions' behavior
of the BP-registered application "auth"
during client-server interaction through HTML templates.
"""

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
#
from src import db
from src.auth import bp
from src.auth.forms import LoginForm, ProfileForm, RegistrationForm, ResetPasswordForm, RequestResetForm
from src.auth.models import User
#
from src.auth.utils import save_image, send_reset_email


@bp.route("/register", methods=["GET", "POST"])
def register_page():
    """
    The function manages user registration procedure.

    :return str: an HTML template for home page/register page
    """
    if current_user.is_authenticated:
        flash('You are already logged in', category="info")
        return redirect(url_for('main.home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    username=form.username.data, email=form.email.data.lower())  # Using UserMixin, PyCharm flashes error
        user.encrypt_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account for '{form.username.data}' successfully created!", category="primary")
        login_user(user)
        return redirect(url_for("main.home_page"))
    elif request.method == "POST" and not request.form.get('g_recaptcha_response'):
        flash("Don't forget to check the Recaptcha box", category="primary")
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login_page():
    """
    The function manages user login procedure.

    :return str: an HTML template for home page/login page
    """

    if current_user.is_authenticated:
        flash("You are already logged in.", category="info")
        return redirect(url_for('main.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user_by_username = User.query.filter_by(username=form.username_or_email.data).first()
        user_by_email = User.query.filter_by(email=form.username_or_email.data).first()
        user = user_by_username or user_by_email
        # if LOGIN fails
        if not user or not user.verify_password(form.password.data):
            flash('Invalid username or password', category="danger")
            return redirect(url_for('auth.login_page'))  # do not remove: POST-GET-redirect pattern
        # if LOGIN is successful
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')  # dictionary
        flash("Successful login", category="primary")
        return redirect(next_page) if next_page else redirect(url_for("main.home_page"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
def logout():
    """
    The function manages user logout procedure.

    :return str: an HTML template for home page
    """
    if not current_user.is_authenticated:
        flash("You have not logged in yet.", category="info")
        return redirect(url_for('main.home_page'))
    logout_user()
    return redirect(url_for('main.home_page'))


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile_page():
    """
    The function manages user profile view/edit procedure.

    :return str: an HTML template for profile page
    """
    form = ProfileForm()
    if form.validate_on_submit():
        if form.image.data:  # if an avatar is updated
            current_user.image = save_image(form.image.data)
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data.lower()
        db.session.commit()  # TODO: no 'db.session.add' is required when altering a db row
        flash("Account updated", category="primary")
        return redirect(url_for('auth.profile_page'))  # do not remove: POST-GET-redirect pattern
    elif request.method == "GET":  # to see current username and email data when the form is loaded
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for("static", filename=f"avatars/{current_user.image}")
    return render_template("auth/profile.html", image=image, form=form)


@bp.route("/request_reset", methods=["GET", "POST"])
def reset_request_page():
    """
    The function manages user password reset request procedure.

    :return str: an HTML template for reset request page/login page/home page
    """
    if current_user.is_authenticated:
        flash("You are already logged in.", category="info")
        return redirect(url_for('main.home_page'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Check your email address for further instructions.", category="info")
        return redirect(url_for("auth.login_page"))
    return render_template("auth/request_reset.html", form=form)


@bp.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password_page(token):
    """
    The function manages user password reset request procedure.

    :param str token: a unique token to verify the user before password reset
    :return str: an HTML template for reset request page/login page/reset request page
    """
    if current_user.is_authenticated:
        flash("You are already logged in.", category="info")
        return redirect(url_for('main.home_page'))
    user = User.verify_reset_token(token)
    if not user:
        flash("That token is invalid or has already expired", category="secondary")
        return redirect(url_for('auth.reset_request_page'))  # do not remove: POST-GET-redirect pattern
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.encrypt_password(form.password.data)
        db.session.commit()  # TODO: no 'db.session.add' is required when altering a db row
        flash(f"Your password has been successfully updated", category="primary")
        return redirect(url_for("auth.login_page"))
    return render_template("auth/reset_password.html", form=form)
