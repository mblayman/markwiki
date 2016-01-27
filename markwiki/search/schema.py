# Copyright (c) 2016, Matt Layman and contributors

from whoosh import fields


class WikiSchema(fields.SchemaClass):
    '''This describes the content that will be stored in the search index.'''

    # The field boost helps wiki page paths show more prevalently in results
    # since they will also be used as links in the content of other pages.
    path = fields.ID(unique=True, field_boost=2.0, stored=True)

    # The content is stored so that highlights can be extracted to display.
    content = fields.TEXT(stored=True)
