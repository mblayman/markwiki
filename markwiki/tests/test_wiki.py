# Copyright (c) 2016, Matt Layman
'''Tests for the wiki access layer.'''

import unittest

from markwiki.wiki import WikiPage
from markwiki.wiki import WikiSection


class TestWiki(unittest.TestCase):

    def test_gets_sections(self):
        '''Test getting sections out of paths.'''
        page_path = '/One/Two/Three'
        page = WikiPage(page_path)
        sections = page.sections

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].name, 'One')
        self.assertEqual(sections[0].path, 'One')
        self.assertEqual(sections[1].name, 'Two')
        self.assertEqual(sections[1].path, 'One/Two')

        section_path = '/Foo/Bar'
        section = WikiSection(section_path)
        sections = section.sections

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].name, 'Foo')
        self.assertEqual(sections[0].path, 'Foo')
        self.assertEqual(sections[1].name, 'Bar')
        self.assertEqual(sections[1].path, 'Foo/Bar')
