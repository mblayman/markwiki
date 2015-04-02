# Copyright (c) 2015, Matt Layman
'''Tests for the search engine.'''

import os
import tempfile
import unittest

from markwiki.search.engine import SearchEngine


class TestSearchEngine(unittest.TestCase):

    def test_has_index(self):
        tmp = tempfile.mkdtemp()
        engine = SearchEngine(tmp)
        self.assertFalse(engine.has_index())

        os.mkdir(engine.index_dir)
        self.assertTrue(engine.has_index())
