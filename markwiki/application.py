# Copyright (c) 2013, Matt Layman and contributors
'''A simple wiki using Markdown'''

from flask import Flask


class MarkWikiApp(Flask):

    def __init__(self, *args, **kwargs):
        super(MarkWikiApp, self).__init__(*args, **kwargs)

        # Load the default configuration.
        self.config.from_object('markwiki.config')

        # Load production settings from a configuration file.
        loaded = self.config.from_envvar('MARKWIKI_SETTINGS', silent=True)

        if not loaded:
            print(' * MARKWIKI_SETTINGS is not set (or has a bad file path). '
                  'Using defaults ...')

        # Inform the login management to disable logins if no authentication
        # is used.
        if not self.config['AUTHENTICATION']:
            self.config['LOGIN_DISABLED'] = True

        # Allow override of template and static folders
        if 'STATIC_PATH' in self.config:
            self.static_folder = self.config['STATIC_PATH']

        if 'TEMPLATE_PATH' in self.config:
            self.template_folder = self.config['TEMPLATE_PATH']
