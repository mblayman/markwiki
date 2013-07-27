# Copyright (c) 2013, Matt Layman and contributors
'''A simple wiki using Markdown'''

import os
import sys

from flask import Flask

from markwiki.util import bootstrap


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

        # Allow override of template and static folders
        if 'STATIC_PATH' in self.config:
            self.static_folder = self.config['STATIC_PATH']

        if 'TEMPLATE_PATH' in self.config:
            self.template_folder = self.config['TEMPLATE_PATH']


app = MarkWikiApp(__name__)

# Check if the wiki exists and bootstrap if it isn't there.
if not os.path.exists(app.config['WIKI_PATH']):
    bootstrap(app.config['WIKI_PATH'])
else:
    # The wiki path must be a directory.
    if not os.path.isdir(app.config['WIKI_PATH']):
        sys.exit('Sorry, the wiki path must be a directory.')

# Because the import is circular, the importing of the views should be the last
# thing so that there is no temptation to use them and cause craziness.
import markwiki.views
