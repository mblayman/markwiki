# Copyright (c) 2014, Matt Layman
'''Tests for the file system storage.'''

import os
import tempfile
import unittest

from markwiki.storage.fs.user import FileUserStorage


class TestFileUserStorage(unittest.TestCase):

    def setUp(self):
        self.config = {
            'MARKWIKI_HOME': tempfile.mkdtemp()
        }
        self.storage = FileUserStorage(self.config)

    def test_has_path(self):
        self.assertEqual(os.path.join(self.config['MARKWIKI_HOME'], 'users'),
                         self.storage._path, 'Storage has a path root.')

    def test_makes_storage_area(self):
        self.assertFalse(os.path.exists(self.storage._path),
                         'User storage does not exist before initialization.')
        self.storage.initialize()
        self.assertTrue(os.path.exists(self.storage._path),
                        'Construction creates the user storage area in the'
                        ' MarkWiki home.')
