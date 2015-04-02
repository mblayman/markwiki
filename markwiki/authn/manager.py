# Copyright (c) 2015, Matt Layman
'''MarkWiki's authentication manager'''

from flask.ext.login import LoginManager
from werkzeug import security


class MarkWikiLoginManager(LoginManager):

    def __init__(self, *args, **kwargs):
        super(MarkWikiLoginManager, self).__init__(*args, **kwargs)

        self.login_message = 'You must be logged in to do that.'
        self.login_message_category = 'info'
        self.login_view = '/login/'

        # The auth framework needs a 1 parameter function so wrap the user
        # storage instance method.
        def loader(user_id):
            return kwargs['app'].user_storage.find_by_id(user_id)

        self.user_loader(loader)

    def authenticate(self, user, password):
        '''Authenticate the user with the supplied password.'''
        return security.check_password_hash(user.password_digest, password)
