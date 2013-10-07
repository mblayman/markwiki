# Copyright (c) 2013, Matt Layman and contributors
'''A simple wiki using Markdown'''

import os
import sys

from markwiki.application import MarkWikiApp
from markwiki.util import bootstrap, bootstrap_auth

# The app is so super special that it needs to come before many imports.
# Basically, only the app class itself and bootstrapping should be imported
# before this.
app = MarkWikiApp(__name__)

# Check if the MarkWiki exists and bootstrap if it isn't there.
if not os.path.exists(app.config['MARKWIKI_HOME']):
    bootstrap(app)
else:
    # The home path must be a directory.
    if not os.path.isdir(app.config['MARKWIKI_HOME']):
        sys.exit('Sorry, the MarkWiki home path must be a directory.')

# Bootstrapping the authentication should be checked every time in case the
# admin credentials have been updated.
from markwiki.authn.manager import MarkWikiLoginManager
login_manager = MarkWikiLoginManager(app=app)

if app.config.get('AUTHENTICATION'):
    bootstrap_auth(app, login_manager)

# Because the import is circular, the importing of the views should be the last
# thing so that there is no temptation to use them and cause craziness.
import markwiki.views.authn
import markwiki.views.core
import markwiki.views.errors
