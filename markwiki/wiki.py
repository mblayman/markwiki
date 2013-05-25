# Copyright (c) 2013, Matt Layman
'''Functions for handling interaction with wiki pages.'''

from collections import namedtuple
import os

from flask import abort

from markwiki import app

# Data types used by MarkWiki
Page = namedtuple('Page', ['name', 'path'])
Section = namedtuple('Section', ['name', 'path'])


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


def get_sections(page_path):
    '''Extract the sections from the provided page path.'''
    sections = []

    # Drop the wiki page name with this slice.
    section_parts = page_path.split('/')[:-1]
    if len(section_parts) > 0:
        section_path = []
        for part in section_parts:
            section_path.append(part)
            # Put the sections parts together to generate the section path.
            sections.append(Section(part, '/'.join(section_path)))

    return sections


def get_wiki(page_path):
    '''Get the wiki's page path.'''
    return os.path.join(app.config['WIKI_PATH'], page_path + '.md')


def write_wiki(path, content):
    '''Write the wiki content to the path provided. Assumes valid path.'''
    # Determine if the directories are already in place.
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        # This could be nested deeply so make the intermediate directories too.
        try:
            os.makedirs(directory)
        except:
            abort(500)

    try:
        with open(path, 'w') as wiki:
            wiki.write(content)
    except IOError:
        # Something bad happened while writing so report failure.
        abort(500)
