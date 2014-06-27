from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.validators import URL, Required

class ShorterForm(Form):
    url = TextField('URL', [URL(), Required()])
    submit_button = SubmitField('Short this!')

