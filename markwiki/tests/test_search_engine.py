# Copyright (c) 2015, Matt Layman
# -*- coding: utf-8 -*-
'''Tests for the search engine.'''

import os
import tempfile
import unittest

from markwiki.search.engine import SearchEngine


class TestSearchEngine(unittest.TestCase):

    def _make_one(self):
        self.markwiki_home = tempfile.mkdtemp()
        return SearchEngine(self.markwiki_home)

    def test_has_index(self):
        engine = self._make_one()
        self.assertFalse(engine.has_index())

        os.mkdir(engine.index_dir)
        self.assertTrue(engine.has_index())

    def test_creates_index(self):
        engine = self._make_one()
        wiki_path = tempfile.mkdtemp()
        with open(os.path.join(wiki_path, 'test.md'), 'w') as f:
            f.write('*hellØ Markdown world*')

        engine.create_index(wiki_path)

        self.assertTrue(os.path.exists(
            os.path.join(self.markwiki_home, 'search', 'MAIN_WRITELOCK')))
