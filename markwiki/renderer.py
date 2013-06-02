# Copyright (c) 2013, Matt Layman
'''Custom rendering'''

import markdown

from markwiki.wikilinks import MarkWikiLinkExtension

# Create this here so that the render call will not have to instantiate the
# extension every call.
wiki_link_extension = MarkWikiLinkExtension()


def render_markdown(wiki_page):
    '''Render the Markdown from the wiki page provided. Assumes path exists.'''
    with open(wiki_page) as wiki_file:
        text = wiki_file.read()
        extensions = [wiki_link_extension, 'fenced_code', 'codehilite',
                      'toc(anchorlink=True)']
        return markdown.markdown(text, safe_mode='escape',
                                 extensions=extensions, output_format='html5')
