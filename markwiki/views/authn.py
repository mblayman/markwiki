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
from markwiki.forms import LoginForm
from markwiki.validators import validate_login


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        error = validate_login(request.form)
        if error is None:
            login_user(User(form.username.data))
            flash('You\'ve logged in.', category='success')

            # 'next' will be defined if the user was coming from another page.
            return redirect(form.next.data or url_for('index'))
        else:
            flash(error)

    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
