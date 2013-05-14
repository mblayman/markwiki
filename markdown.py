# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os
import shutil

from flask import Flask
from flask import render_template
# TODO: Make an extension to replace wiki words with links.

# Globals - The very few
app = Flask(__name__)
here = os.path.abspath(os.path.dirname(__file__))
# The location of all wiki content
wiki_path = ''

def bootstrap():
    '''Bootstrap the wiki with some basic content.'''
    # Create the wiki at the specified path.
    os.makedirs(wiki_path)

    # Populate the wiki with the main page.
    markwiki = 'MarkWiki.md'
    markwiki_source = os.path.join(here, 'templates', markwiki)
    shutil.copy(markwiki_source, os.path.join(wiki_path, markwiki))

def get_wiki(page_path):
    '''Get the wiki's page path.'''
    return os.path.join(wiki_path, page_path + '.md')

@app.route('/')
def index():
    '''Display the MarkWiki main page.'''
    return wiki('MarkWiki')

@app.route('/wiki/')
@app.route('/wiki/<path:page_path>')
def wiki(page_path='MarkWiki'):
    '''Render the wiki page or make a new one if the wiki doesn't exist.'''
    wiki_page = get_wiki(page_path)
    # TODO: Fetch the wiki page from the site, render it and
    # insert it into the template.

    # Always use the last name in the path as the title.
    title = os.path.split(page_path)[-1]

    return render_template('wiki.html', title=title)

if __name__ == '__main__':
    # TODO: Make the wiki location configurable.
    home = os.path.expanduser('~')
    wiki_path = os.path.join(home, '.markwiki')

    # Check if the wiki exists and bootstrap if it isn't there.
    if not os.path.exists(wiki_path):
        bootstrap()

    app.debug = True
    app.run(host='0.0.0.0')

