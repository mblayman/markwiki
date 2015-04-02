# Copyright (c) 2015, Matt Layman
'''Validate aspects of MarkWiki.'''

import os

from markwiki import app
from markwiki.exceptions import ValidationError


def is_valid_section(section_path):
    '''Check if the section path is valid.'''
    return os.path.isdir(os.path.join(app.config['WIKI_PATH'], section_path))


def validate_directories(directories):
    '''Check that the directories are sane.'''
    for directory in directories:
        # Prevent any double, triple, or however many slashes in a row.
        if directory == '':
            raise ValidationError(
                'It looks like there were multiple slashes in a row in your '
                'wiki name.')

        # No relative paths allowed.
        if directory in ['..', '.']:
            raise ValidationError(
                'Wiki names can\'t include just \'..\' or \'.\' between '
                'slashes.')

        # None of the directory parts can end in '.md' because that would
        # screw up the ability to make a wiki in the directory that has the
        # same name.
        if directory.endswith('.md'):
            raise ValidationError(
                "Wiki names can't end in '.md' in the parts before the last "
                "slash. Sorry, this rule is weird. I know.")


def validate_page_path(page_path):
    '''Check that the page path is valid.'''
    # An empty page path is no good.
    if page_path is None or page_path == '':
        raise ValidationError('You need to supply some wiki name.')

    # Do some directory checking.
    page_parts = page_path.split('/')
    if len(page_parts) > 1:
        validate_directories(page_parts[:-1])
