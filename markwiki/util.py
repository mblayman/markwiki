# Copyright (c) 2013, Matt Layman
'''The junk drawer. A place for methods that don't logically fit elsewhere.'''

import os
import shutil


def bootstrap(app):
    '''Bootstrap the wiki with some basic content.'''
    here = os.path.abspath(os.path.dirname(__file__))

    # Copy all the help content.
    wiki_path = app.config['WIKI_PATH']
    markwiki_help = os.path.join(here, 'templates', 'MarkWiki')
    shutil.copytree(markwiki_help, os.path.join(wiki_path, 'MarkWiki'))

    # Populate the wiki with the main page.
    home_source = os.path.join(markwiki_help, 'Introduction.md')
    shutil.copy(home_source, os.path.join(wiki_path, 'Home.md'))

    if app.config.get('AUTHENTICATION'):
        bootstrap_auth(app)


def bootstrap_auth(app):
    '''Bootstrap all the necessary authentication support if it is enabled.'''
    # TODO: Create the auth section and save the admin credentials.
