# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os
import shutil

from flask import abort
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import markdown
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

def render_markdown(wiki_page):
    '''Render the Markdown from the wiki page provided. Assumes path exists.'''
    with open(wiki_page) as wiki_file:
        text = wiki_file.read()
        return markdown.markdown(text, safe_mode='escape')

def write_wiki(path, content):
    '''Write the wiki content to the path provided. Assumes valid path.'''
    # TODO: Make sure all the intermediate directories exist.
    try:
        with open(path, 'w') as wiki:
            wiki.write(content)
        return True
    except IOError:
        # Something bad happened while writing so report failure.
        return False

def valid_page_path(page_path):
    '''Check that the page path is valid.'''
    # An empty page path is no good.
    if page_path is None or page_path == '':
        return False

    # Neither is a path that uses relative path stuff.
    # TODO: implement this check

    # None of the directory parts can end in '.md' because that would screw
    # up the ability to make a wiki in the directory that has the same name.
    # TODO: implement this check

    return True

@app.errorhandler(500)
def internal_server_error(error):
    '''Display a 500 page.'''
    return render_template('internal_server_error.html')

@app.route('/')
def index():
    '''Display the MarkWiki main page.'''
    return wiki('MarkWiki')

@app.route('/create/')
@app.route('/create/<path:page_path>')
def create(page_path=None):
    '''Display the wiki creation form.'''
    return render_template('create.html', page_path=page_path)

@app.route('/make_wiki', methods=['POST'])
def make_wiki():
    '''Make the wiki page.'''
    page_path = request.form['page_path']
    if valid_page_path(page_path):
        wiki_page = get_wiki(page_path)

        # Proceed if the wiki does not exist.
        if not os.path.exists(wiki_page):
            success = write_wiki(wiki_page, request.form['wiki_content'])
            if success:
                return redirect(url_for('wiki', page_path=page_path))
            else:
                abort(500)
        else:
            # TODO: Report back that the page already exists.
            pass
    else:
        # TODO: Report that the path is not valid.
        pass

@app.route('/wiki/')
@app.route('/wiki/<path:page_path>')
def wiki(page_path='MarkWiki'):
    '''Render the wiki page or make a new one if the wiki doesn't exist.'''
    wiki_html = ''

    wiki_page = get_wiki(page_path)
    if os.path.isfile(wiki_page):
        wiki_html = render_markdown(wiki_page)
    else:
        return create(page_path)

    # Always use the last name in the path as the title.
    title = os.path.split(page_path)[-1]

    return render_template('wiki.html', title=title, wiki=wiki_html)

if __name__ == '__main__':
    # TODO: Make the wiki location configurable.
    home = os.path.expanduser('~')
    wiki_path = os.path.join(home, '.markwiki')

    # Check if the wiki exists and bootstrap if it isn't there.
    if not os.path.exists(wiki_path):
        bootstrap()

    # TODO: Not production ready yet. Debug is on and dangerous.
    app.debug = True
    app.run(host='0.0.0.0')

