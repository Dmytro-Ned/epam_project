from flask_login import current_user
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, Optional, ValidationError
#
from src.auth.models import User


class RegistrationForm(FlaskForm):
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

    def validate_username(self, input_username):  # do not make @static
        user = User.query.filter_by(username=input_username.data).first()
        if user:
            raise ValidationError("A user with such a username already exists. Input another one.")
        if input_username.data.lower() in ['admin', 'administrator']:
            raise ValidationError("Forbidden username")

    def validate_email(self, input_email):  # do not make @static
        user = User.query.filter_by(email=input_email.data).first()
        if user:
            raise ValidationError("A user with such an email already exists. Input another one.")


class LoginForm(FlaskForm):
    username_or_email = StringField('Enter your Username or Email', validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Enter your Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign Up')


class ProfileForm(FlaskForm):
    first_name = StringField('Update your First Name', validators=[Length(min=2, max=20), Optional()])
    last_name = StringField('Update your Last Name', validators=[Length(min=2, max=40), Optional()])
    username = StringField('Update your Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField('Update your Email', validators=[DataRequired(), Email()])
    image = FileField('Update your Avatar', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, input_username):  # do not make @static
        if input_username.data != current_user.username:
            user = User.query.filter_by(username=input_username.data).first()
            if user:
                raise ValidationError("A user with that username already exists. Input another one.")
        if input_username.data.lower() in ['admin', 'administrator']:
            raise ValidationError("Forbidden username")

    def validate_email(self, input_email):  # do not make @static
        if input_email.data != current_user.email:
            user = User.query.filter_by(email=input_email.data).first()
            if user:
                raise ValidationError("A user with that email already exists. Input another one.")


class RequestResetForm(FlaskForm):
    email = StringField('Enter your Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request a reset')

    def validate_email(self, input_email):  # do not make @static
        user = User.query.filter_by(email=input_email.data).first()
        if not user:
            raise ValidationError("Such address does not exist.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter your Password', validators=[DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm your Password', validators=[DataRequired(), Length(min=8),
                                                                 EqualTo('password',
                                                                         message='Passwords do not match')
                                                                 ]
                            )
    submit = SubmitField('Reset')
