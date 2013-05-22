# Copyright (c) 2013, Matt Layman
'''The default configuration for MarkWiki'''

import os

# Production configurations should override this setting and not debug.
DEBUG = True
# The app needs a secret key to use flash messages.
SECRET_KEY = 'It\'s a secret to everybody.'
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
# The location of all wiki content
WIKI_PATH = os.path.join(os.path.expanduser('~'), '.markwiki')

