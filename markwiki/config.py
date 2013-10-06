# Copyright (c) 2013, Matt Layman
'''The default configuration for MarkWiki'''

import os

# Production configurations should override this setting and not debug.
DEBUG = True

AUTHENTICATION = None
ADMINISTRATOR = None
ADMIN_PASSWORD = None

# The app needs a secret key to use flash messages.
SECRET_KEY = 'It\'s a secret to everybody.'

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000

# The location of all MarkWiki information
MARKWIKI_HOME = os.path.join(os.path.expanduser('~'), '.markwiki')

# Advanced settings
STATIC_PATH = None
TEMPLATE_PATH = None
