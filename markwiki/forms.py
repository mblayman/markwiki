# Copyright (c) 2016, Matt Layman
'''Forms used by MarkWiki'''

from flask.ext.wtf import Form
from wtforms.fields import HiddenField
from wtforms.fields import PasswordField
from wtforms.fields import StringField
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

from markwiki import app


def is_new_user(form, field):
    if app.user_storage.find_by_name(field.data) is not None:
        raise ValidationError('Sorry, that user already exists.')


class AddUserForm(Form):
    username = StringField('Username', [
        InputRequired('You did not provide a username.'),
        Length(max=80, message='Sorry, the max length of a username is 80.'),
        is_new_user
    ])


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


class RegisterForm(Form):
    username = StringField('Username', [
        InputRequired('You did not provide a username.'),
        Length(max=80, message='Sorry, the max length of a username is 80.'),
        is_new_user
    ])

    password = PasswordField('Password', [
        InputRequired('You did not provide a password.'),
        EqualTo('confirm', message='The passwords must match.'),
        Length(min=8, message=(
            'Passwords less than 8 characters are really not safe. '
            'Please choose something longer.'
        )),
    ])

    confirm = PasswordField('Repeat password')
