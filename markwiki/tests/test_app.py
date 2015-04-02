# Copyright (c) 2015, Matt Layman
'''Tests for the core application.'''

import os
import tempfile
import unittest

from markwiki.application import MarkWikiApp


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = MarkWikiApp('test')

    def test_is_bootstrapped(self):
        tmp = tempfile.mkdtemp()
        open(os.path.join(tmp, self.app.bootstrapped_token_file), 'w').close()
        self.app.config['MARKWIKI_HOME'] = tmp
        self.assertTrue(self.app.is_bootstrapped())

        self.app.config['MARKWIKI_HOME'] = 'something_unlikely_to_exist'
        self.assertFalse(self.app.is_bootstrapped())
