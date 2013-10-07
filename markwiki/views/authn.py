# Copyright (c) 2013, Matt Layman
'''The authentication views'''

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

from markwiki import app
from markwiki import login_manager
from markwiki.authn.user import User
from markwiki.forms import LoginForm


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = validate_login(form)
        if error is None:
            login_user(User(form.username.data))
            flash('You\'ve logged in.', category='success')

            # 'next' will be defined if the user was coming from another page.
            return redirect(form.next.data or url_for('index'))
        else:
            flash(error)

    return render_template('login.html', form=form)


def validate_login(form):
    '''Validate the user login from the provided form. A valid login produces
    no error messages so None is a valid user.'''
    if not login_manager.has_user(form.username.data):
        return 'That username is not valid.'

    if not login_manager.authenticate(form.username.data, form.password.data):
        return 'You\'ve entered an incorrect password.'

    return None


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
