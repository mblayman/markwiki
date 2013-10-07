# Copyright (c) 2013, Matt Layman
'''The junk drawer. A place for methods that don't logically fit elsewhere.'''

import os
import shutil
import sys


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


def bootstrap_auth(app, login_manager):
    '''Bootstrap all the necessary authentication support if it is enabled.'''
    # Ensure the auth storage area exists.
    if not os.path.exists(app.config['AUTH_PATH']):
        os.makedirs(app.config['AUTH_PATH'])

    # Check that the admin credentials are valid.
    if not app.config.get('ADMINISTRATOR'):
        sys.exit('You did not provide an administrator username.')

    if not app.config.get('ADMIN_PASSWORD'):
        sys.exit('You did not provide an administrator password.')

    # Store the credentials of the admin account.
    login_manager.add_user(app.config['ADMINISTRATOR'],
                           app.config['ADMIN_PASSWORD'])
