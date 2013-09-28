# Copyright (c) 2013, Matt Layman
'''A model of MarkWiki users'''

from flask.ext.login import UserMixin


class User(UserMixin):

    @staticmethod
    def get(userid):
        '''Factory method to produce a user instance'''
        return User(userid)

    def __init__(self, id):
        self.id = id
