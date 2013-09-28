# Copyright (c) 2013, Matt Layman
'''The authentication views'''

from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user

from markwiki import app
from markwiki.authn.user import User


@app.route('/login/')
def login():
    # TODO: implement login form and validation.
    login_user(User('mblayman'))
    flash('You\'ve logged in.')
    return redirect('/')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')
