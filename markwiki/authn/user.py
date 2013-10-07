# Copyright (c) 2013, Matt Layman
'''A model of MarkWiki users'''

from flask.ext.login import AnonymousUserMixin
from flask.ext.login import UserMixin

from markwiki import app


class AnonymousUser(AnonymousUserMixin):

    def is_admin(self):
        return False


class User(UserMixin):

    @staticmethod
    def get(userid):
        '''Factory method to produce a user instance'''
        return User(userid)

    def __init__(self, id):
        self.id = id

    def is_admin(self):
        return self.get_id() == app.config['ADMINISTRATOR']
