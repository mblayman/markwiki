# Copyright (c) 2013, Matt Layman and contributors
'''A simple wiki using Markdown'''

import os
import sys

from markwiki.application import MarkWikiApp
from markwiki.authn.manager import MarkWikiLoginManager
from markwiki.util import bootstrap


app = MarkWikiApp(__name__)
login_manager = MarkWikiLoginManager(app)

# Check if the MarkWiki exists and bootstrap if it isn't there.
if not os.path.exists(app.config['MARKWIKI_HOME']):
    bootstrap(app)
else:
    # The home path must be a directory.
    if not os.path.isdir(app.config['MARKWIKI_HOME']):
        sys.exit('Sorry, the MarkWiki home path must be a directory.')

# Because the import is circular, the importing of the views should be the last
# thing so that there is no temptation to use them and cause craziness.
import markwiki.views.authn
import markwiki.views.core
import markwiki.views.errors
