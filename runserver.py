# Copyright (c) 2013, Matt Layman
'''Run MarkWiki.'''

from markwiki import app

app.run(app.config['SERVER_HOST'], app.config['SERVER_PORT'])

