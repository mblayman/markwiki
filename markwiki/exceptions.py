# Copyright (c) 2015, Matt Layman
'''MarkWiki exceptions'''


class ConfigurationError(Exception):
    '''An exception to raise when an error occurred from misconfiguration.'''


class UserStorageError(Exception):
    '''An error occurred in the user storage service.'''


class ValidationError(Exception):
    '''A simple exception to use to report errors to users.'''
