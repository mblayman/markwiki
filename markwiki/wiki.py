# Copyright (c) 2013, Matt Layman
'''Functions for handling interaction with wiki pages.'''

from collections import namedtuple
import os

from markwiki import app
from markwiki.renderer import render_markdown

# Data types used by MarkWiki
Page = namedtuple('Page', ['name', 'path'])
Section = namedtuple('Section', ['name', 'path'])


class WikiPage(object):
    '''A model to represent a wiki page'''

    def __init__(self, page_path):
        self.page_path = page_path
        self._wiki_path = None

    @property
    def content(self):
        '''Get the source content of the page.'''
        with open(self.wiki_path, 'r') as wiki:
            return wiki.read()

    @property
    def exists(self):
        '''Check if the page actually exists.'''
        return os.path.isfile(self.wiki_path)

    @property
    def html(self):
        '''Render the page for display.'''
        return render_markdown(self.wiki_path)

    @property
    def sections(self):
        '''Extract the sections from the page path.'''
        # Drop the wiki page name with this slice.
        section_parts = self.page_path.split('/')[:-1]
        return _get_sections_from_parts(section_parts)

    @property
    def title(self):
        # Always use the last name in the path as the title.
        return os.path.split(self.page_path)[-1]

    @property
    def wiki_path(self):
        '''Get the wiki's page path.'''
        if not self._wiki_path:
            self._wiki_path = os.path.join(app.config['WIKI_PATH'],
                                           self.page_path + '.md')
        return self._wiki_path

    def store(self, content):
        '''Write the content. Assumes valid path. Returns success status.'''
        # Determine if the directories are already in place.
        directory = os.path.dirname(self.wiki_path)
        if not os.path.exists(directory):
            # This could be nested deeply so make all intermediate directories.
            try:
                os.makedirs(directory)
            except:
                return False

        try:
            with open(self.wiki_path, 'w') as wiki:
                wiki.write(content)
        except IOError:
            # Something bad happened while writing so report failure.
            return False

        return True

    def delete(self):
        try:
            os.remove(self.wiki_path)
        except:
            return False

        return True


def get_section_content(section_path):
    '''Get the sections and pages in this section. Assumes valid section.'''
    pages = []
    sections = []
    section_directory = os.path.join(app.config['WIKI_PATH'], section_path)
    contents = os.listdir(section_directory)
    contents.sort()
    for content in contents:
        if content.endswith('.md'):
            # Trim the extension.
            page_name = content[:-3]
            pages.append(Page(page_name,
                              os.path.join(section_path, page_name)))
        else:
            sections.append(Section(content,
                            os.path.join(section_path, content)))

    return (sections, pages)


def get_sections_from(section_path):
    '''Extract the sections from the provided section path.'''
    return _get_sections_from_parts(section_path.split('/'))


def _get_sections_from_parts(section_parts):
    '''Transform the section parts into sections usable by view templates.'''
    sections = []

    section_path = []
    for part in section_parts:
        if part is '':
            continue

        section_path.append(part)
        # Put the sections parts together to generate the section path.
        sections.append(Section(part, '/'.join(section_path)))

    return sections
