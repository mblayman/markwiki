# Copyright (c) 2015, Matt Layman
'''Tests for the User model.'''

import unittest

from markwiki.models.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User('mblayman', 'test@123.com', 'password', 'digest')

    def test_has_login_type(self):
        self.assertEqual('password', self.user.login_type)

    def test_has_name(self):
        self.assertEqual('mblayman', self.user.name)

    def test_has_email(self):
        self.assertEqual('test@123.com', self.user.email)

    def test_has_password_digest(self):
        self.assertEqual('digest', self.user.password_digest)
