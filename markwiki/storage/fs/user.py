# Copyright (c) 2014, Matt Layman

import json
import hashlib
import os

from markwiki.exceptions import UserStorageError
from markwiki.storage.user import UserStorage


class FileUserStorage(UserStorage):
    '''A file system based user storage'''

    def __init__(self, config):
        self._path = os.path.join(config['MARKWIKI_HOME'], 'users')

    def initialize(self):
        if not os.path.exists(self._path):
            os.mkdir(self._path)

    def create(self, user):
        '''Create a new user by storing it as JSON on the file system.'''
        m = hashlib.md5()
        m.update(user.name)
        user_path = os.path.join(self._path, m.hexdigest())

        if os.path.exists(user_path):
            raise UserStorageError('A user with that name already exists.')

        json_data = json.dumps(user.__dict__, sort_keys=True, indent=2,
                               separators=(',', ': '))
        with open(user_path, 'w') as f:
            f.write(json_data)
