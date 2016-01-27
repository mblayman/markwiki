# Copyright (c) 2016, Matt Layman
'''A model of MarkWiki users'''


class User(object):

    def __init__(self, name, email, login_type, password_digest, user_id=None):
        self.name = name
        self.email = email
        self.login_type = login_type
        self.password_digest = password_digest
        self.user_id = user_id

    # The methods below are to satisfy the API of the auth framework.
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id
