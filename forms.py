from flask_wtf import Form
from wtforms import TextField, SubmitField

class ShorterForm(Form):
    url = TextField('URL')
    submit_button = SubmitField('Short this!')

