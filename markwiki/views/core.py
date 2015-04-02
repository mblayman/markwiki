# Copyright (c) 2015, Matt Layman
'''The views that MarkWiki displays'''

from flask import abort
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import login_required

from markwiki import app
from markwiki.exceptions import ValidationError
from markwiki.validators import is_valid_section, validate_page_path
from markwiki.wiki import WikiPage
from markwiki.wiki import WikiSection


def render_wiki_editor(page):
    '''Render the wiki editor with content from the provided wiki page.
    Assumes a valid wiki page.'''
    try:
        return render_template('edit.html', page_path=page.page_path,
                               wiki_content=page.content)
    except IOError:
        abort(500)


@app.route('/')
def index():
    '''Display the MarkWiki main page.'''
    return wiki('Home')


@app.route('/create/')
@app.route('/create/<path:page_path>')
@login_required
def create(page_path=None, wiki_content=None):
    '''Display the wiki creation form.'''
    return render_template('create.html', page_path=page_path,
                           wiki_content=wiki_content)


@app.route('/make_wiki', methods=['POST'])
@login_required
def make_wiki():
    '''Make the wiki page.'''
    page_path = request.form['page_path']
    content = request.form['wiki_content']
    try:
        validate_page_path(page_path)
        page = WikiPage(page_path)

        # Proceed if the wiki does not exist.
        if not page.exists:
            if not page.store(content):
                # Storing would fail if something unrecoverable happened.
                abort(500)

            app.search_engine.add_wiki(page_path, content)

            return redirect(url_for('wiki', page_path=page_path))
        else:
            flash('That wiki name already exists. Please choose another.')
            return create(page_path, request.form['wiki_content'])
    except ValidationError as verror:
        flash(verror.message)
        return create(page_path, request.form['wiki_content'])


@app.route('/edit/')
@app.route('/edit/<path:page_path>')
@login_required
def edit(page_path=None):
    '''Edit a wiki page.'''
    # It should be possible to create a new page from the edit link.
    if page_path is None:
        return redirect(url_for('create'))

    try:
        validate_page_path(page_path)
        page = WikiPage(page_path)

        # Proceed if the wiki exists.
        if page.exists:
            return render_wiki_editor(page)
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
@login_required
def update_wiki():
    '''Update a wiki page.'''
    # If the path changed, then this is now a new page.
    if request.form['original_page_path'] != request.form['page_path']:
        return make_wiki()
    else:
        # Because the path is the same as the original, then it must be valid
        # because it is a pre-existing page.
        page_path = request.form['page_path']
        page = WikiPage(page_path)
        if not page.store(request.form['wiki_content']):
            # Storing would fail if something unrecoverable happened.
            abort(500)

        app.search_engine.update_wiki(page_path,
                                      request.form['wiki_content'])

        return redirect(url_for('wiki', page_path=page_path))


@app.route('/wiki/')
@app.route('/wiki/<path:page_path>/')
def wiki(page_path='Home'):
    '''Render the wiki page or make a new one if the wiki doesn't exist.'''
    page = WikiPage(page_path)
    if page.exists:
        g.sections = page.sections
        return render_template('wiki.html', page_path=page_path,
                               title=page.title, wiki=page.html)
    else:
        return create(page_path)


@app.route('/list/')
@app.route('/list/<path:section_path>/')
def list(section_path=''):
    '''List the contents of a directory section.'''
    if is_valid_section(section_path):
        section = WikiSection(section_path)
        g.sections = section.sections
        return render_template('list.html', section_path=section_path,
                               sections=section.subsections,
                               pages=section.pages)
    else:
        # This should only happen if a wiki link is created with a bad section
        # or if someone directly tries to attempt a bad URL.
        flash('Sorry. That wiki section doesn\'t exist.')
        return redirect(url_for('index'))


@app.route('/delete/<path:page_path>', methods=['POST'])
@login_required
def delete(page_path):
    '''Delete the wiki page.'''
    if page_path == 'Home':
        flash('You sneaky devil. You can\'t delete the main page. '
              'But feel free to edit it.')
        return redirect(url_for('index'))

    try:
        validate_page_path(page_path)
        page = WikiPage(page_path)

        if page.exists:
            if not page.delete():
                # Unsuccessful delete.
                abort(500)

            app.search_engine.delete_wiki(page_path)
        else:
            flash('That wiki doesn\'t exist.')
    except ValidationError as verror:
        # The user tried to delete a bogus page straight from the URL.
        flash(verror.message)

    return redirect(url_for('index'))


@app.route('/search/')
def search():
    user_query = request.args.get('q', '')
    results = app.search_engine.search(user_query)
    return render_template('search.html', user_query=user_query,
                           results=results)
