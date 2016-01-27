# Copyright (c) 2016, Matt Layman

from abc import ABCMeta
from abc import abstractmethod


class UserStorage(object):
    '''An abstract interface that all user storage services must implement'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config):
        '''The constructor will be supplied the application's configuration.'''

    @abstractmethod
    def initialize(self):
        '''Initialization will occur shortly after construction so the service
        can perform any initial setup before it is used by the application.'''

    @abstractmethod
    def create(self, user):
        '''Create a new user. Raise ``UserStorageError`` on failure.'''

    @abstractmethod
    def find_by_email(self, email):
        '''Find a user by email. Return ``None`` if no such user exists.'''

    @abstractmethod
    def find_by_id(self, user_id):
        '''Find a user by ID. Return ``None`` if no such user exists.'''

    @abstractmethod
    def find_by_name(self, name):
        '''Find a user by name. Return ``None`` if no such user exists.'''

    @abstractmethod
    def update(self, user):
        '''Update an existing user. Raise ``UserStorageError`` on failure.'''
