# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os
import shutil

from flask import abort
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import markdown

from wikilinks import MarkWikiLinkExtension

# Globals - The very few
app = Flask(__name__)
here = os.path.abspath(os.path.dirname(__file__))
# The location of all wiki content
wiki_path = ''

# The app needs a secret key to use flash messages. If more serious session
# management is needed then the secret key will have to handled better.
app.secret_key = 'It\'s a secret to everybody.'

class ValidationError(Exception):
    '''A simple exception to use to report errors to users.'''

def bootstrap():
    '''Bootstrap the wiki with some basic content.'''
    # TODO: copy all help files to the wiki area.
    # Create the wiki at the specified path.
    os.makedirs(wiki_path)

    # Populate the wiki with the main page.
    markwiki = 'MarkWiki.md'
    markwiki_source = os.path.join(here, 'templates', markwiki)
    shutil.copy(markwiki_source, os.path.join(wiki_path, markwiki))

def build_wiki_url(label, base, end):
    '''Build the wiki URL for the WikiLinkExtension.'''
    return url_for('wiki', page_path=label)

def get_wiki(page_path):
    '''Get the wiki's page path.'''
    return os.path.join(wiki_path, page_path + '.md')

def render_markdown(wiki_page):
    '''Render the Markdown from the wiki page provided. Assumes path exists.'''
    with open(wiki_page) as wiki_file:
        text = wiki_file.read()
        extensions = [wiki_link_extension, 'fenced_code', 'codehilite']
        return markdown.markdown(text, safe_mode='escape',
            extensions=extensions, output_format='html5' )

def render_wiki_editor(page_path, wiki_page):
    '''Render the wiki editor with content from the provided wiki page.
    Assumes a valid wiki page path.'''
    try:
        with open(wiki_page, 'r') as wiki:
            wiki_content = wiki.read()
            return render_template('edit.html', page_path=page_path,
                wiki_content=wiki_content)
    except IOError:
        abort(500)

    # Some weird stuff happened if we got here.
    abort(500)

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

def validate_directories(directories):
    '''Check that the directories are sane.'''
    for directory in directories:
        # Prevent any double, triple, or however many slashes in a row.
        if directory == '':
            raise ValidationError('It looks like there were multiple slashes '
                'in a row in your wiki name.')

        # No relative paths allowed.
        if directory in ['..', '.']:
            raise ValidationError('Wiki names can\'t include just \'..\' or '
                '\'.\' between slashes.')

        # None of the directory parts can end in '.md' because that would
        # screw up the ability to make a wiki in the directory that has the
        # same name.
        if directory.endswith('.md'):
            raise ValidationError("Wiki names can't end in '.md' in the parts "
                "before the last slash. Sorry, this rule is weird. I know.")

def validate_page_path(page_path):
    '''Check that the page path is valid. Return an '''
    # An empty page path is no good.
    if page_path is None or page_path == '':
        raise ValidationError('You need to supply some wiki name.')

    # Do some directory checking.
    page_parts = page_path.split('/')
    if len(page_parts) > 1:
        validate_directories(page_parts[:-1])

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
def create(page_path=None, wiki_content=None):
    '''Display the wiki creation form.'''
    return render_template('create.html', page_path=page_path,
        wiki_content=wiki_content)

@app.route('/make_wiki', methods=['POST'])
def make_wiki():
    '''Make the wiki page.'''
    page_path = request.form['page_path']
    try:
        validate_page_path(page_path)
        wiki_page = get_wiki(page_path)

        # Proceed if the wiki does not exist.
        if not os.path.exists(wiki_page):
            write_wiki(wiki_page, request.form['wiki_content'])
            return redirect(url_for('wiki', page_path=page_path))
        else:
            flash('That wiki name already exists. Please choose another.')
            return create(page_path, request.form['wiki_content'])
    except ValidationError as verror:
        flash(verror.message)
        return create(page_path, request.form['wiki_content'])

@app.route('/edit/')
@app.route('/edit/<path:page_path>')
def edit(page_path=None):
    '''Edit a wiki page.'''
    # It should be possible to create a new page from the edit link.
    if page_path is None:
        return redirect(url_for('create'))

    try:
        validate_page_path(page_path)
        wiki_page = get_wiki(page_path)

        # Proceed if the wiki exists.
        if os.path.exists(wiki_page):
            return render_wiki_editor(page_path, wiki_page)
        else:
            # Get the user going with this new page.
            return redirect(url_for('create', page_path=page_path))
    except ValidationError as verror:
        # The user tried to create a page straight from the URL, but the path
        # isn't correct. Give them the page path again in case they fat
        # fingered something.
        flash(verror.message)
        return redirect(url_for('create', page_path=page_path))

@app.route('/update_wiki', methods=['POST'])
def update_wiki():
    '''Update a wiki page.'''
    # If the path changed, then this is now a new page.
    if request.form['original_page_path'] != request.form['page_path']:
        return make_wiki()
    else:
        # Because the path is the same as the original, then it must be valid
        # because it is a pre-existing page.
        page_path = request.form['page_path']
        wiki_page = get_wiki(page_path)
        write_wiki(wiki_page, request.form['wiki_content'])
        return redirect(url_for('wiki', page_path=page_path))

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

    return render_template('wiki.html', page_path=page_path, title=title,
        wiki=wiki_html)

@app.route('/delete/<path:page_path>')
def delete(page_path):
    '''Delete the wiki page.'''
    if page_path == 'MarkWiki':
        flash('You sneaky devil. You can\'t delete the main page. '
            'But feel free to edit it.')

    try:
        validate_page_path(page_path)
        wiki_page = get_wiki(page_path)

        # Proceed if the wiki exists.
        if os.path.exists(wiki_page):
            os.remove(wiki_page)
        else:
            flash('That wiki doesn\'t exist.')
    except ValidationError as verror:
        # The user tried to delete a bogus page straight from the URL.
        flash(verror.message)

    return redirect(url_for('index'))

if __name__ == '__main__':
    # TODO: Make the wiki location configurable.
    home = os.path.expanduser('~')
    wiki_path = os.path.join(home, '.markwiki')
    wiki_link_extension = MarkWikiLinkExtension(configs={
        'build_url': build_wiki_url
    })

    # Check if the wiki exists and bootstrap if it isn't there.
    if not os.path.exists(wiki_path):
        bootstrap()

    # TODO: Not production ready yet. Debug is on and dangerous.
    app.debug = True
    app.run(host='0.0.0.0')

