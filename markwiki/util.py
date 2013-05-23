# Copyright (c) 2013, Matt Layman
'''The junk drawer. A place for methods that don't logically fit elsewhere.'''

import os
import shutil


def bootstrap(wiki_path):
    '''Bootstrap the wiki with some basic content.'''
    here = os.path.abspath(os.path.dirname(__file__))

    # Copy all the help content.
    markwiki_help = os.path.join(here, 'templates', 'MarkWiki')
    shutil.copytree(markwiki_help, os.path.join(wiki_path, 'MarkWiki'))

    # Populate the wiki with the main page.
    markwiki_source = os.path.join(markwiki_help, 'Introduction.md')
    shutil.copy(markwiki_source, os.path.join(wiki_path, 'MarkWiki.md'))
