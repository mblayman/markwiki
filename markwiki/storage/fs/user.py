# Copyright (c) 2014, Matt Layman

import json
import hashlib
import os

from markwiki.exceptions import UserStorageError
from markwiki.models.user import User
from markwiki.storage.user import UserStorage


class FileUserStorage(UserStorage):
    '''A file system based user storage'''


    def __init__(self, config):
        self._path = os.path.join(config['MARKWIKI_HOME'], 'users')
        # An index of user ID to user file paths
        self._id_index_file = os.path.join(self._path, 'id.index')
        self._id_index = {}

    def initialize(self):
        if not os.path.exists(self._path):
            os.mkdir(self._path)
            self._write_json(self._id_index, self._id_index_file)

    def create(self, user):
        '''Create a new user by storing it as JSON on the file system.'''
        user_file = self._get_user_file(user.name)

        if os.path.exists(user_file):
            raise UserStorageError('A user with that name already exists.')

        # TODO: validate that the username and email are not in use already.

        # Everything looks good so get the user an ID and save it.
        user.user_id = self._generate_user_id()
        self._write_json(user.__dict__, user_file)

        # Now that the user is saved, update the indices.
        self._update_indices(user, user_file)

    def find_by_id(self, user_id):
        '''Find a user by their ID or return ``None``.'''
        user_file = self._id_index.get(user_id)
        if user_file is None:
            return None

        if os.path.exists(user_file):
            with open(user_file, 'r') as f:
                data = json.loads(f.read())
                return User(data['name'], data['email'], data['login_type'],
                            data['password_digest'], data['user_id'])

        return None

    def _generate_user_id(self):
        '''Generate a unique user ID.'''
        # Because there might be multiple workers (like if running with
        # gunicorn), refresh the in-memory indices to avoid ID clashes.
        self._read_indices()
        user_id = len(self._id_index)
        while self.find_by_id(unicode(user_id)) is not None:
            user_id += 1

        # The auth system will try to do lookups with unicode so the key might
        # as well be unicode to be consistent.
        return unicode(user_id)

    def _get_user_file(self, name):
        '''Get the file path where the user's data will be stored.'''
        m = hashlib.md5()
        m.update(name)
        return os.path.join(self._path, m.hexdigest())

    def _read_indices(self):
        '''Read the file indices into memory.'''
        with open(self._id_index_file, 'r') as f:
            self._id_index = json.loads(f.read())

    def _update_indices(self, user, user_file):
        '''Update the file indices with the provided user information.'''
        self._id_index[user.user_id] = user_file
        self._write_json(self._id_index, self._id_index_file)

    def _write_json(self, data, out):
        '''Write out JSON with common settings.'''
        json_data = json.dumps(data, sort_keys=True, indent=2,
                               separators=(',', ': '))
        with open(out, 'w') as f:
            f.write(json_data)
