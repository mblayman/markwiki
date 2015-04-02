# Copyright (c) 2015, Matt Layman
'''Run MarkWiki.'''

import argparse
import sys

from markwiki import app
from markwiki.freezer import freeze


def run():
    '''Run the application.

    This run wrapper is to work with setuptools entry points. This provides the
    `markwiki` command.
    '''
    description = 'A simple wiki using Markdown'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-f', '--freeze',
        nargs='?',
        const='frozen',  # When flag is provided, but no path is given.
        default=None,  # When no flag is provided.
        help='generate an archive version of the MarkWiki and store it in '
             'the DESTINATION directory (default: frozen)',
        dest='freezer_destination',
        metavar='DESTINATION'
    )

    args = parser.parse_args()

    # If a freezer destination was specified, then the wiki should be frozen.
    if args.freezer_destination:
        status = freeze(args.freezer_destination)
        # Quit after the wiki is frozen.
        sys.exit(status)

    app.run(app.config['SERVER_HOST'], app.config['SERVER_PORT'])
