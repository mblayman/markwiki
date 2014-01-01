# Copyright (c) 2013, Matt Layman and contributors
'''A simple wiki using Markdown'''

import os

from flask import Flask

from markwiki.search.engine import SearchEngine
from markwiki import util


class MarkWikiApp(Flask):

    # Configuration settings that are booleans
    boolean_settings = [
        'ALLOW_REGISTRATION',
        'DEBUG',
    ]

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
        self.config['AUTH_PATH'] = os.path.join(self.config['MARKWIKI_HOME'],
                                                'auth')

        # Inform the login management to disable logins if no authentication
        # is used.
        if not self.config['AUTHENTICATION']:
            self.config['LOGIN_DISABLED'] = True

        # Allow override of template and static folders
        if self.config['STATIC_PATH']:
            self.static_folder = self.config['STATIC_PATH']

        if self.config['TEMPLATE_PATH']:
            self.template_folder = self.config['TEMPLATE_PATH']

        self.search_engine = SearchEngine(self.config['MARKWIKI_HOME'])

    def _load_from_environment(self):
        '''Load any config options from the environment if they exist.'''
        for key in sorted(self.config.keys()):
            if os.environ.get(key) is not None:
                print('Using \'{key}\' from environment ...'.format(key=key))

                if key in self.boolean_settings:
                    self.config[key] = util.boolify(os.environ[key])
                else:
                    self.config[key] = os.environ[key]
