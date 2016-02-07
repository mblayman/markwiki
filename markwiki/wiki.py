# Copyright (c) 2016, Matt Layman
'''Functions for handling interaction with wiki pages.'''

from collections import namedtuple
import io
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
        self._rel_path = None

    @property
    def content(self):
        '''Get the source content of the page.'''
        with io.open(self.wiki_path, 'r', encoding='utf-8') as wiki:
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

    @property
    def rel_path(self):
        '''Get the relative path.'''
        if not self._rel_path:
            self._rel_path = self.page_path + '.md'
        return self._rel_path

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
            with open(self.wiki_path, 'wb') as wiki:
                # get rid of any Windows-like ending
                wiki.write(content.encode('utf-8').replace('\r\n', '\n'))
        except IOError:
            # Something bad happened while writing so report failure.
            return False
        if app.config['GIT_ENABLED']:
            app.gitint.update_file(self.rel_path)

        return True

    def delete(self):
        try:
            os.remove(self.wiki_path)
        except:
            return False

        return True


class WikiSection(object):
    '''A model for wiki sections'''

    def __init__(self, section_path):
        self.section_path = section_path
        # Not using an empty list to start because there could legitimately be
        # no pages or subsections and the cache would retry every property call
        # if it only checked for empty lists.
        self._pages = None
        self._subsections = None

    @property
    def pages(self):
        if self._pages is None:
            self._get_section_content()

        return self._pages

    @property
    def sections(self):
        '''Sections include everything above and including this section.'''
        return _get_sections_from_parts(self.section_path.split('/'))

    @property
    def subsections(self):
        if self._subsections is None:
            self._get_section_content()

        return self._subsections

    def _get_section_content(self):
        '''Get subsections and pages in this section. Assumes valid section.'''
        self._pages = []
        self._subsections = []
        directory = os.path.join(app.config['WIKI_PATH'], self.section_path)
        contents = os.listdir(directory)
        contents.sort()
        for content in contents:
            if content.endswith('.md'):
                # Trim the extension.
                page_name = content[:-3]
                self._pages.append(Page(page_name,
                                   os.path.join(self.section_path, page_name)))
            elif not content.startswith('.'):
                self._subsections.append(
                    Section(content, os.path.join(self.section_path, content)))


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
