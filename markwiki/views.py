# Copyright (c) 2013, Matt Layman
'''The views that MarkWiki displays'''

import os

from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from markwiki import app
from markwiki.exceptions import ValidationError
from markwiki.renderer import render_markdown
from markwiki.validators import is_valid_section, validate_page_path
from markwiki.wiki import get_section_content
from markwiki.wiki import get_sections_from_page_path
from markwiki.wiki import get_sections_from_section_path
from markwiki.wiki import get_wiki, write_wiki


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


@app.errorhandler(500)
def internal_server_error(error):
    '''Display a 500 page.'''
    return render_template('internal_server_error.html')


@app.route('/')
def index():
    '''Display the MarkWiki main page.'''
    return wiki('Home')


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
@app.route('/wiki/<path:page_path>/')
def wiki(page_path='Home'):
    '''Render the wiki page or make a new one if the wiki doesn't exist.'''
    wiki_html = ''

    wiki_page = get_wiki(page_path)
    if os.path.isfile(wiki_page):
        wiki_html = render_markdown(wiki_page)
    else:
        return create(page_path)

    # Always use the last name in the path as the title.
    title = os.path.split(page_path)[-1]

    # Get the sections if there are any.
    g.sections = get_sections_from_page_path(page_path)

    return render_template('wiki.html', page_path=page_path, title=title,
                           wiki=wiki_html)


@app.route('/list/')
@app.route('/list/<path:section_path>/')
def list(section_path=''):
    '''List the contents of a directory section.'''
    if is_valid_section(section_path):
        # Get the sections here and above.
        g.sections = get_sections_from_section_path(section_path)

        (sections, pages) = get_section_content(section_path)
        return render_template('list.html', section_path=section_path,
                               sections=sections, pages=pages)
    else:
        # This should only happen if a wiki link is created with a bad section
        # or if someone directly tries to attempt a bad URL.
        flash('Sorry. That wiki section doesn\'t exist.')
        return redirect(url_for('index'))


@app.route('/delete/<path:page_path>')
def delete(page_path):
    '''Delete the wiki page.'''
    if page_path == 'Home':
        flash('You sneaky devil. You can\'t delete the main page. '
              'But feel free to edit it.')
        return redirect(url_for('index'))

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
