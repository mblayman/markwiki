# Copyright (c) 2013, Matt Layman
'''MarkWiki's authentication manager'''

from flask.ext.login import LoginManager

from markwiki.authn.user import User


class MarkWikiLoginManager(LoginManager):

    def __init__(self, *args, **kwargs):
        super(MarkWikiLoginManager, self).__init__(*args, **kwargs)

        # All custom configuration for the login manager should be here.
        self.login_message = 'You must be logged in to do that.'
        self.login_view = '/login/'
        self.user_loader(User.get)
