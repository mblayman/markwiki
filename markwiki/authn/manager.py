# Copyright (c) 2013, Matt Layman
'''MarkWiki's authentication manager'''

import hashlib
import os

from flask.ext.login import LoginManager
from werkzeug import security

from markwiki.authn.user import AnonymousUser
from markwiki.authn.user import User


class MarkWikiLoginManager(LoginManager):

    def __init__(self, *args, **kwargs):
        super(MarkWikiLoginManager, self).__init__(*args, **kwargs)

        # Keep a reference to the app. This introduces a bi-directional
        # link, but the manager uses the app to get config information.
        self.app = kwargs['app']

        # All custom configuration for the login manager should be here.
        self.anonymous_user = AnonymousUser
        self.login_message = 'You must be logged in to do that.'
        self.login_message_category = 'info'
        self.login_view = '/login/'
        self.user_loader(User.get)

    def add_user(self, username, password):
        '''Add a user to auth storage.'''
        with open(self._get_user_path(username), 'w') as creds:
            pwhash = security.generate_password_hash(password)
            creds.write(pwhash)

    def authenticate(self, username, password):
        '''Authenticate the user with the supplied password. Assume that the
        username is valid.'''
        with open(self._get_user_path(username)) as creds:
            pwhash = creds.read()
            return security.check_password_hash(pwhash, password)

    def has_user(self, username):
        '''Check if the user exists in the auth storage.'''
        return os.path.exists(self._get_user_path(username))

    def _get_user_path(self, username):
        '''Get the storage location of the user.'''
        m = hashlib.md5()
        m.update(username)
        return os.path.join(self.app.config['AUTH_PATH'], m.hexdigest())
