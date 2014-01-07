# Copyright (c) 2014, Matt Layman
'''Tests for the StorageFactory.'''

import unittest

from markwiki.exceptions import ConfigurationError
from markwiki.storage.factory import UserStorageFactory
from markwiki.storage.fs.user import FileUserStorage


class InitializeException(Exception):
    '''An exception to ensure storage initialization was invoked.'''


class FakeUserStorage(object):

    def __init__(self, config):
        '''Do nothing.'''

    def initialize(self):
        raise InitializeException()


class TestUserStorageFactory(unittest.TestCase):

    def setUp(self):
        self.factory = UserStorageFactory()

    def test_get_storage(self):
        config = {
            'MARKWIKI_HOME': 'nothing',
            'STORAGE_TYPE': 'file'
        }

        storage = self.factory._get_storage(config)
        self.assertTrue(isinstance(storage, FileUserStorage))

    def test_invalid_storage(self):
        config = {}
        self.assertRaises(ConfigurationError, self.factory.get_storage, config)

    def test_storage_initializes(self):
        config = {'STORAGE_TYPE': 'file'}
        types = {'file': FakeUserStorage}
        factory = UserStorageFactory(storage_types=types)
        self.assertRaises(InitializeException, factory.get_storage, config)
