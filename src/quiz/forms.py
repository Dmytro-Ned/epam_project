"""
This module renders forms for templates
displaying fields for "Option" model
in the process of updating of the "Result" ORM instance
(taking a test).
"""

from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField


class OptionMultiForm(FlaskForm):
    """
    A class which renders a form for "Option" display.

    Fields: options(RadioMultiField)
    """
    options = RadioField("Option", choices=[])
    submit = SubmitField('Submit')
