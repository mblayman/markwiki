# Copyright (c) 2014, Matt Layman

import os

from markwiki.storage.user import UserStorage


class FileUserStorage(UserStorage):
    '''A file system based user storage'''

    def __init__(self, config):
        self._path = os.path.join(config['MARKWIKI_HOME'], 'users')

    def initialize(self):
        if not os.path.exists(self._path):
            os.mkdir(self._path)
