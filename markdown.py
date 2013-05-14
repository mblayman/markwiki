# Copyright (c) 2013, Matt Layman
'''A simple wiki using Markdown'''

import os

from flask import Flask
from flask import render_template
# TODO: Make an extension to replace wiki words with links.

app = Flask(__name__)

@app.route('/')
def index():
    '''Display the MarkWiki main page.'''
    # TODO: Fetch the MarkWiki from the site, render it into Markdown and
    # insert it into the template.
    return wiki('MarkWiki')

@app.route('/wiki/')
@app.route('/wiki/<path:page_path>')
def wiki(page_path='MarkWiki'):
    '''Render the wiki page or make a new one if the wiki doesn't exist.'''

    # Always use the last name in the path as the title.
    title = os.path.split(page_path)[-1]

    return render_template('wiki.html', title=title)

if __name__ == '__main__':
    # TODO: Make sure a wiki site is created and populated with the MarkWiki.
    app.debug = True
    app.run(host='0.0.0.0')

