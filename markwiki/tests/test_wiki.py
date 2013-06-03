# Copyright (c) 2013, Matt Layman
'''Tests for the wiki access layer.'''

import unittest

from markwiki.wiki import get_sections_from_page_path
from markwiki.wiki import get_sections_from_section_path


class TestWiki(unittest.TestCase):

    def test_gets_sections(self):
        '''Test getting sections out of paths.'''
        page_path = '/One/Two/Three'
        sections = get_sections_from_page_path(page_path)

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].name, 'One')
        self.assertEqual(sections[0].path, 'One')
        self.assertEqual(sections[1].name, 'Two')
        self.assertEqual(sections[1].path, 'One/Two')

        section_path = '/Foo/Bar'
        sections = get_sections_from_section_path(section_path)

        self.assertEqual(len(sections), 2)
        self.assertEqual(sections[0].name, 'Foo')
        self.assertEqual(sections[0].path, 'Foo')
        self.assertEqual(sections[1].name, 'Bar')
        self.assertEqual(sections[1].path, 'Foo/Bar')
