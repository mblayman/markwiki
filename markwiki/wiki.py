# Copyright (c) 2013, Matt Layman
'''Functions for handling interaction with wiki pages.'''

import os

from flask import abort

from markwiki import app

def get_wiki(page_path):
    '''Get the wiki's page path.'''
    return os.path.join(app.config['WIKI_PATH'], page_path + '.md')

def write_wiki(path, content):
    '''Write the wiki content to the path provided. Assumes valid path.'''
    # Determine if the directories are already in place.
    directory = os.path.dirname(path)
    if  not os.path.exists(directory):
        # This could be nested deeply so make the intermediate directories too.
        try:
            os.makedirs(directory)
        except:
            abort(500)

    try:
        with open(path, 'w') as wiki:
            wiki.write(content)
    except IOError:
        # Something bad happened while writing so report failure.
        abort(500)

