# Copyright (c) 2015, Matt Layman and contributors
'''A simple wiki using Markdown'''

from markwiki.application import build_app
from markwiki.util import bootstrap_auth

# The app is so super special that it needs to come before many imports.
# Basically, only the app class itself and bootstrapping should be imported
# before this.
app = build_app(__name__)

# Bootstrapping the authentication should be checked every time in case the
# admin credentials have been updated.
from markwiki.authn.manager import MarkWikiLoginManager  # NOQA
login_manager = MarkWikiLoginManager(app=app)

if app.config.get('AUTHENTICATION'):
    bootstrap_auth(app)

# Ensure that the search engine is available.
app.search_engine.open_index()

# Because the import is circular, the importing of the views should be the last
# thing so that there is no temptation to use them and cause craziness.
import markwiki.views.authn  # NOQA
import markwiki.views.core  # NOQA
import markwiki.views.errors  # NOQA
