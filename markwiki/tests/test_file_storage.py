# Copyright (c) 2014, Matt Layman
'''Tests for the file system storage.'''

import hashlib
import json
import os
import tempfile
import unittest

from markwiki.exceptions import UserStorageError
from markwiki.models.user import User
from markwiki.storage.fs.user import FileUserStorage


class TestFileUserStorage(unittest.TestCase):

    def setUp(self):
        self.config = {
            'MARKWIKI_HOME': tempfile.mkdtemp()
        }
        self.storage = FileUserStorage(self.config)
        self.storage.initialize()

    def test_has_path(self):
        self.assertEqual(os.path.join(self.config['MARKWIKI_HOME'], 'users'),
                         self.storage._path, 'Storage has a path root.')

    def test_makes_storage_area(self):
        config = {
            'MARKWIKI_HOME': tempfile.mkdtemp()
        }
        storage = FileUserStorage(config)
        self.assertFalse(os.path.exists(storage._path),
                         'User storage does not exist before initialization.')
        storage.initialize()
        self.assertTrue(os.path.exists(storage._path),
                        'Construction creates the user storage area in the'
                        ' MarkWiki home.')

    def test_create(self):
        user = User('mblayman', 'test@123.com', 'password', 'passwd_digest')
        self.storage.create(user)

        m = hashlib.md5()
        m.update('mblayman')
        user_path = os.path.join(self.storage._path, m.hexdigest())
        self.assertTrue(os.path.exists(user_path), 'The user was stored.')

    def test_create_fails_with_existing_user(self):
        user = User('mblayman', 'test@123.com', 'password', 'passwd_digest')
        self.storage.create(user)

        self.assertRaises(UserStorageError, self.storage.create, user)

    def test_create_generates_id(self):
        user = User('mblayman', 'test@123.com', 'password', 'passwd_digest')
        self.storage.create(user)
        self.assertEqual(u'0', user.user_id)

        user = User('laymanmb', '123@test.com', 'password', 'passwd_digest')
        self.storage.create(user)
        self.assertEqual(u'1', user.user_id)
