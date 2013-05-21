# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os
import shutil

from flask import Flask

app = Flask(__name__)

# TODO: Not production ready yet. Debug is on and dangerous.
app.debug = True

# The app needs a secret key to use flash messages. If more serious session
# management is needed then the secret key will have to handled better.
app.secret_key = 'It\'s a secret to everybody.'

# TODO: Make the wiki location configurable.
home = os.path.expanduser('~')
wiki_path = os.path.join(home, '.markwiki')

# The location of all wiki content
app.config['WIKI_PATH'] = wiki_path

import markwiki.views

def bootstrap():
    '''Bootstrap the wiki with some basic content.'''
    here = os.path.abspath(os.path.dirname(__file__))

    # Copy all the help content.
    markwiki_help = os.path.join(here, 'templates', 'MarkWiki')
    shutil.copytree(markwiki_help, os.path.join(wiki_path, 'MarkWiki'))

    # Populate the wiki with the main page.
    markwiki_source = os.path.join(markwiki_help, 'Introduction.md')
    shutil.copy(markwiki_source, os.path.join(wiki_path, 'MarkWiki.md'))

# Check if the wiki exists and bootstrap if it isn't there.
if not os.path.exists(wiki_path):
    bootstrap()

