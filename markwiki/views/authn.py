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
from markwiki.authn.user import User
from markwiki.validators import validate_login


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Add the check for the form in case the user is being redirected from a
    # login_required page.
    if request.form:
        error = validate_login(request.form)
        if error is None:
            login_user(User(request.form['user_name']))
            flash('You\'ve logged in.')

            # 'next' will be defined if the user was coming from another page.
            return redirect(request.form.get('next') or url_for('index'))
        else:
            flash(error)

    return render_template('login.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
