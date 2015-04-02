# Copyright (c) 2015, Matt Layman
'''The default configuration for MarkWiki'''

import os

# Developers may set debug to True to get reloading and other debug support.
DEBUG = False

# Use simple file system storage by default.
STORAGE_TYPE = 'file'

AUTHENTICATION = None
ADMINISTRATOR = None
ADMIN_PASSWORD = None
ALLOW_REGISTRATION = True

# The app needs a secret key to use flash messages.
SECRET_KEY = 'It\'s a secret to everybody.'

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000

# The location of all MarkWiki information
MARKWIKI_HOME = os.path.join(os.path.expanduser('~'), '.markwiki')

# Advanced settings
STATIC_PATH = None
TEMPLATE_PATH = None
