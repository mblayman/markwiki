# Copyright (c) 2013, Matt Layman
'''Forms used by MarkWiki'''

from flask.ext.wtf import Form
from wtforms.fields import HiddenField
from wtforms.fields import PasswordField
from wtforms.fields import StringField
from wtforms.validators import InputRequired
from wtforms.validators import Length


class LoginForm(Form):
    username = StringField('Username', [
        InputRequired('You did not provide a username.'),
        Length(max=80, message='Sorry, the max length of a username is 80.')
    ])

    password = PasswordField('Password', [
        InputRequired('You did not provide a password.')
    ])

    # 'next' is used by Flask-Login to handle redirects.
    next = HiddenField()
