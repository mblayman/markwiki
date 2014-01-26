# Copyright (c) 2013, Matt Layman
'''The authentication views'''

from flask import abort
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
import requests
from werkzeug import security

from markwiki import app
from markwiki import login_manager
from markwiki import util
from markwiki.authn.user import User
from markwiki.forms import AddUserForm
from markwiki.forms import LoginForm
from markwiki.forms import RegisterForm
from markwiki.models.user import User


@app.route('/administrate/')
@login_required
def administrate():
    if current_user.name != app.config['ADMINISTRATOR']:
        flash('You don\'t have permission to do that.')
        return redirect(url_for('index'))

    return render_template('administrate.html')


@app.route('/add_user/', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.name != app.config['ADMINISTRATOR']:
        flash('You don\'t have permission to do that.')
        return redirect(url_for('index'))

    form = AddUserForm()
    if form.validate_on_submit():
        password = util.generate_password()
        pwhash = security.generate_password_hash(password)
        user = User(form.username.data,
                    '',  # Email is not used.
                    'password',
                    pwhash)
        app.user_storage.create(user)
        return render_template('user_confirmation.html',
                               username=form.username.data,
                               password=password)

    return render_template('add_user.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if not app.config['ALLOW_REGISTRATION']:
        flash('You don\'t have permission to do that.')
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        pwhash = security.generate_password_hash(form.password.data)
        user = User(form.username.data,
                    '',  # Email is not used.
                    'password',
                    pwhash)
        app.user_storage.create(user)
        login_user(user)

        message = (
            'Hi, {username}. You\'ve successfully registered!'.format(
                username=form.username.data)
        )
        flash(message, category='success')

        # Do a redirect so a refresh won't attempt to add the user again.
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = validate_login(form)
        if error is None:
            user = app.user_storage.find_by_name(form.username.data)
            login_user(user)
            flash('You\'ve logged in.', category='success')

            # 'next' will be defined if the user was coming from another page.
            return redirect(form.next.data or url_for('index'))
        else:
            flash(error)

    return render_template('login.html', form=form)


def validate_login(form):
    '''Validate the user login from the provided form. A valid login produces
    no error messages so None is a valid user.'''
    user = app.user_storage.find_by_name(form.username.data)
    if user is None:
        return 'That username is not valid.'

    if not login_manager.authenticate(user, form.password.data):
        return 'You\'ve entered an incorrect password.'

    return None


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
