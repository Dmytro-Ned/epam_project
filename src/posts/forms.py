"""
This module renders forms for templates
displaying fields for "Post" model
in the process of creation, viewing and editing.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    A class which renders a form for "Post" creataion.

    Fields: title, related test, content(text)
    """
    title = StringField('Title', validators=[DataRequired()])
    test = SelectField('Test', choices=[], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Confirm')
