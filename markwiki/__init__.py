# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os
import sys

from flask import Flask

from markwiki.util import bootstrap

app = Flask(__name__)

# Load the default configuration.
app.config.from_object('markwiki.config')

# Load production settings from a configuration file.
app.config.from_envvar('MARKWIKI_SETTINGS', silent=True)

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

