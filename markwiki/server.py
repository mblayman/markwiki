# Copyright (c) 2013, Matt Layman
'''Run MarkWiki.'''

from markwiki import app


def run():
    '''Run the application.

    This run wrapper is to work with setuptools entry points. This provides the
    `markwiki` command.
    '''
    app.run(app.config['SERVER_HOST'], app.config['SERVER_PORT'])
