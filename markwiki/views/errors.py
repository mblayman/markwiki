# Copyright (c) 2015, Matt Layman
'''The error views'''

from flask import render_template

from markwiki import app


@app.errorhandler(405)
def method_not_allowed(error):
    '''Display a 405 page.'''
    return render_template('method_not_allowed.html')


@app.errorhandler(500)
def internal_server_error(error):
    '''Display a 500 page.'''
    return render_template('internal_server_error.html')
