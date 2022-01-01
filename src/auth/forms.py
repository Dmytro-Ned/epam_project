"""
This module renders forms for templates
displaying fields for "User" model
in the process of registration, authorization,
profile viewing/editing and password changing.
"""

from string import punctuation
#
from flask_login import current_user
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional, ValidationError
#
from src.auth.models import User


class RegistrationForm(FlaskForm):
    """
    A class which renders a form for "User" registration.

    Fields: first name, last name, username, email address, password
    Methods:
        - validate_username
        - validate_email
    """
    first_name = StringField('Enter your First Name', validators=[Length(min=2, max=20), Optional()])
    last_name = StringField('Enter your Last Name', validators=[Length(min=2, max=40), Optional()])
    username = StringField('Enter your Username', validators=[DataRequired(), InputRequired(), Length(min=2, max=20)])
    email = EmailField('Enter your Email', validators=[DataRequired(), InputRequired(), Email()])
    password = PasswordField('Enter your Password', validators=[DataRequired(), InputRequired(), Length(min=8)])
    confirm_pass = PasswordField('Confirm your Password', validators=[DataRequired(), Length(min=8),
                                                                      EqualTo('password',
                                                                              message='Passwords do not match')
                                                                      ]
                                 )
    recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    # def validate_username(self, input_username):  # do not make @static
    #     """
    #     This method verifies that input username would not break SQL constraints,
    #     is unique, does not contain forbidden characters and differs from
    #     the administrator's username.
    #     Raises ValidationErrors otherwise.
    #
    #     :param StringField input_username: a username input into the field
    #     """
    #     user = User.query.filter_by(username=input_username.data).first()
    #     if user:
    #         raise ValidationError("A user with such a username already exists. Input another one.")
    #     for char in input_username.data:
    #         forbidden_chars = punctuation + " "
    #         if char in forbidden_chars:
    #             raise ValidationError(f"Forbidden characters: {forbidden_chars}")
    #     if input_username.data.lower() in ['admin', 'administrator']:
    #         raise ValidationError("Forbidden username")

    def validate_email(self, input_email):  # do not make @static
        """
        This method verifies that input email address would not break SQL constraints,
        is unique and does contain proper characters.
        Raises ValidationErrors otherwise.

        :param EmailField input_email: an email address input into the field
        """
        user = User.query.filter_by(email=input_email.data).first()
        if user:
            raise ValidationError("A user with such an email already exists. Input another one.")


class LoginForm(FlaskForm):
    """
    A class which renders a form for User login.

    Fields: username or email address, password
    """
    username_or_email = StringField('Enter your Username or Email', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Enter your Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign Up')


class ProfileForm(FlaskForm):
    """
    A class which renders a form for User profile view/edit.

    Fields: first name, last name, username, email address, avatar picture
    Methods:
        - validate_username
        - validate_email
    """
    first_name = StringField('Update your First Name', validators=[Length(min=2, max=20), Optional()])
    last_name = StringField('Update your Last Name', validators=[Length(min=2, max=40), Optional()])
    username = StringField('Update your Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Update your Email', validators=[DataRequired(), Email()])
    image = FileField('Update your Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, input_username):  # do not make @static
        """
        This method verifies that input username would not break SQL constraints,
        is unique, does not contain forbidden characters and differs from
        the administrator's username.
        Raises ValidationErrors otherwise.

        :param StringField input_username: a username input into the field
        """
        if input_username.data != current_user.username:
            user = User.query.filter_by(username=input_username.data).first()
            if user:
                raise ValidationError("A user with that username already exists. Input another one.")
            for char in input_username.data:
                forbidden_chars = punctuation + " "
                if char in forbidden_chars:
                    raise ValidationError(f"Forbidden characters: {forbidden_chars}")
            if input_username.data.lower() in ['admin', 'administrator']:
                raise ValidationError("Forbidden username")

    def validate_email(self, input_email):  # do not make @static
        """
        This method verifies that input email address would not break SQL constraints,
        is unique and does contain proper characters.
        Raises ValidationErrors otherwise.

        :param EmailField input_email: an email address input into the field
        """
        if input_email.data != current_user.email:
            user = User.query.filter_by(email=input_email.data).first()
            if user:
                raise ValidationError("A user with that email already exists. Input another one.")


class RequestResetForm(FlaskForm):
    """
    A class which renders a form for User password reset request.

    Fields: email address
    Methods:
        - validate_email
    """
    email = StringField('Enter your Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request a reset')

    def validate_email(self, input_email):  # do not make @static
        """
        This method verifies that input email address would not break SQL constraints,
        is unique and does contain proper characters.
        Raises ValidationErrors otherwise.

        :param EmailField input_email: an email address input into the field
        """
        user = User.query.filter_by(email=input_email.data).first()
        if not user:
            raise ValidationError("Such address does not exist.")


class ResetPasswordForm(FlaskForm):
    """
    A class which renders a form for User password reset.

    Fields: new password
    """
    password = PasswordField('Enter your Password', validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm your Password', validators=[DataRequired(), Length(min=8),
                                                                 EqualTo('password',
                                                                         message='Passwords do not match')
                                                                 ]
                            )
    submit = SubmitField('Reset')
