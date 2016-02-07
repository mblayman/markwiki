# Copyright (c) 2016, Matt Layman and contributors
'''A simple wiki using Markdown'''

import os

from flask import Flask

from markwiki.git.git_integration import GitIntegration
from markwiki.search.engine import SearchEngine
from markwiki.storage.factory import UserStorageFactory
from markwiki import util


def build_app(app_name):
    '''Build the application and extend it with various services.'''
    app = MarkWikiApp(app_name)

    if not app.is_bootstrapped():
        print('This appears to be a new MarkWiki. Adding initial content ...')
        util.bootstrap(app)

    # Extend the app with the search engine.
    app.search_engine = SearchEngine(app.config['MARKWIKI_HOME'])
    if not app.search_engine.has_index():
        app.search_engine.create_index(app.config['WIKI_PATH'])

    user_storage_factory = UserStorageFactory()
    app.user_storage = user_storage_factory.get_storage(app.config)

    app.gitint = None
    if app.config['GIT_ENABLED']:
        app.gitint = GitIntegration(app.config['WIKI_PATH'])

    return app


class MarkWikiApp(Flask):

    # Configuration settings that are booleans
    boolean_settings = [
        'ALLOW_REGISTRATION',
        'DEBUG',
    ]

    # For file stroage, the bootstrap token acts as an indicator that the wiki
    # has been bootstrapped before.
    bootstrapped_token_file = '.bootstrapped'

    def __init__(self, *args, **kwargs):
        super(MarkWikiApp, self).__init__(*args, **kwargs)

        # Load the default configuration.
        self.config.from_object('markwiki.config')

        # Load production settings from a configuration file.
        loaded = self.config.from_envvar('MARKWIKI_SETTINGS', silent=True)

        if not loaded:
            print('MARKWIKI_SETTINGS is not set or has a bad path. '
                  'Using defaults ...')

        self._load_from_environment()

        # Set the locations for derived paths like the wiki storage area.
        self.config['WIKI_PATH'] = os.path.join(self.config['MARKWIKI_HOME'],
                                                'wiki')

        # Inform the login management to disable logins if no authentication
        # is used.
        if not self.config['AUTHENTICATION']:
            self.config['LOGIN_DISABLED'] = True

        # Allow override of template and static folders
        if self.config['STATIC_PATH']:
            self.static_folder = self.config['STATIC_PATH']

        if self.config['TEMPLATE_PATH']:
            self.template_folder = self.config['TEMPLATE_PATH']

    def _load_from_environment(self):
        '''Load any config options from the environment if they exist.'''
        for key in sorted(self.config.keys()):
            if os.environ.get(key) is not None:
                print('Using \'{key}\' from environment ...'.format(key=key))

                if key in self.boolean_settings:
                    self.config[key] = util.boolify(os.environ[key])
                else:
                    self.config[key] = os.environ[key]

    def is_bootstrapped(self):
        return os.path.exists(os.path.join(self.config['MARKWIKI_HOME'],
                                           self.bootstrapped_token_file))
