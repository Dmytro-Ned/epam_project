from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField


class OptionMultiForm(FlaskForm):
    options = RadioField("Option", choices=[])
    submit = SubmitField('Submit')
