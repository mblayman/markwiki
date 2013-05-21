# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os
import sys

from flask import Flask

from markwiki.util import bootstrap

# Production configurations should override this setting and not debug.
DEBUG = True
# The app needs a secret key to use flash messages.
SECRET_KEY = 'It\'s a secret to everybody.'
# The location of all wiki content
WIKI_PATH = os.path.join(os.path.expanduser('~'), '.markwiki')

app = Flask(__name__)

# Load all the capitalized variables defined here as configuration.
app.config.from_object(__name__)

# Load production setting from a configuration file.
# TODO: use from_envvar

# Check if the wiki exists and bootstrap if it isn't there.
if not os.path.exists(WIKI_PATH):
    bootstrap(WIKI_PATH)
else:
    # The wiki path must be a directory.
    if not os.path.isdir(WIKI_PATH):
        sys.exit('Sorry, the wiki path must be a directory.')

# Because the import is circular, the importing of the views should be the last
# thing so that there is no temptation to use them and cause craziness.
import markwiki.views

