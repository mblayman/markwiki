# Copyright (c) 2015, Matt Layman
'''Freeze the default MarkWiki site for documentation.'''

import os
import shutil
import tempfile

from flask_frozen import Freezer

from markwiki import app


def freeze(destination):
    '''Freeze the wiki to the destination directory.'''
    # If the freezer is provided a relative URL then it behaves by trying to
    # write to package area. This won't work if the package is installed so
    # convert the relative path to an absolute one.
    if not os.path.isabs(destination):
        destination = os.path.join(os.getcwd(), destination)

    # Set MarkWiki in a freezing mode so that certain elements of the views
    # won't get rendered.
    app.config['FREEZING'] = True

    app.config['FREEZER_IGNORE_MIMETYPE_WARNINGS'] = True
    app.config['FREEZER_DESTINATION'] = destination

    # The freeze operation is destructive because it follows the delete
    # links. Copy the wiki into a temporary area and work with that instead.
    _create_wiki_copy()

    freezer = Freezer(app)

    # Add the URL generator to suppress a warning. It won't really do anything.
    @freezer.register_generator
    def delete():
        yield {'page_path': 'Home'}

    try:
        freezer.freeze()
    except OSError:
        return ('Failed to freeze the MarkWiki. Do you have permission to '
                'write to the destination directory?')

    return _prune_frozen(destination)


def _create_wiki_copy():
    '''Create a copy of the wiki and alter the wiki path to point to it.'''
    temp_dir = tempfile.mkdtemp()
    wiki_copy = os.path.join(temp_dir, 'wiki')
    shutil.copytree(app.config['WIKI_PATH'], wiki_copy)

    app.config['WIKI_PATH'] = wiki_copy


def _prune_frozen(destination):
    '''Prune out parts of the frozen output that won't work. Basically, all
    the stuff not related to viewing.'''
    unneeded_directories = ['create', 'edit', 'delete']
    for directory in unneeded_directories:
        shutil.rmtree(os.path.join(destination, directory))
