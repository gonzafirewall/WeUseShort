from flask_wtf import Form
from wtforms import TextField, SubmitField, PasswordField
from wtforms.validators import URL, Required


class ShorterForm(Form):
    url = TextField('URL', [URL(), Required()])
    submit_button = SubmitField('Short this!')


class UserForm(Form):
    username = TextField('User', [Required()])
    password = PasswordField('Password', [Required()])
    submit_button = SubmitField('Enter')
