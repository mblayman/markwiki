# Copyright (c) 2016, Matt Layman
'''A set of factories to generate storage services based on configuration'''

from markwiki.exceptions import ConfigurationError
from markwiki.storage.fs.user import FileUserStorage


class UserStorageFactory(object):

    available_storage_types = {
        'file': FileUserStorage
    }

    def __init__(self, storage_types=None):
        self.types = storage_types
        if self.types is None:
            self.types = self.available_storage_types

    def get_storage(self, config):
        '''Get the storage and initialize it.'''
        storage = self._get_storage(config)
        storage.initialize()
        return storage

    def _get_storage(self, config):
        '''Build a user storage service for the app's configuration.'''
        storage_cls = self.types.get(config.get('STORAGE_TYPE'))
        if storage_cls is not None:
            return storage_cls(config)
        else:
            raise ConfigurationError('An invalid storage type was specified.')
