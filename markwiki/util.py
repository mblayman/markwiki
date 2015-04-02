# Copyright (c) 2015, Matt Layman
'''The junk drawer. A place for methods that don't logically fit elsewhere.'''

import os
import random
import shutil
import string
import sys

from werkzeug import security

from markwiki.models.user import User


def boolify(value):
    '''Check the string value for boolean-like behavior and return a bool.'''
    return value.lower().startswith('t')


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

    token = os.path.join(app.config['MARKWIKI_HOME'],
                         app.bootstrapped_token_file)
    with open(token, 'w') as f:
        f.write('Bootstrapping is complete. Do not delete this file.')


def bootstrap_auth(app):
    '''Bootstrap all the necessary authentication support if it is enabled.'''
    # Check that the admin credentials are valid.
    if not app.config.get('ADMINISTRATOR'):
        sys.exit('You did not provide an administrator username.')

    if not app.config.get('ADMIN_PASSWORD'):
        sys.exit('You did not provide an administrator password.')

    # Store the credentials of the admin account.
    admin = app.user_storage.find_by_name(app.config['ADMINISTRATOR'])
    if admin is None:
        pwhash = security.generate_password_hash(app.config['ADMIN_PASSWORD'])
        # No admin for this account name so create one.
        admin = User(app.config['ADMINISTRATOR'],
                     '',  # The admin does not use email.
                     'password',
                     pwhash)
        app.user_storage.create(admin)
    else:
        # The configuration file may have changed the password so always update
        # the administrator's password.
        pwhash = security.generate_password_hash(app.config['ADMIN_PASSWORD'])
        admin.password_digest = pwhash
        app.user_storage.update(admin)


def generate_password():
    '''Generate a random password.'''
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for i in xrange(12))
