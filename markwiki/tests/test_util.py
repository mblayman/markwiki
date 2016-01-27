# Copyright (c) 2016, Matt Layman
'''Tests for the utility methods.'''

import unittest

from markwiki import util


class TestUtil(unittest.TestCase):

    def test_boolify(self):
        truth = 'True'
        self.assertTrue(util.boolify(truth))
        self.assertEqual(truth, 'True',
                         'Make sure boolify did not mangle the value.')

        self.assertTrue(util.boolify('true'))

        self.assertFalse(util.boolify('False'))
        self.assertFalse(util.boolify('false'))
        self.assertFalse(util.boolify('anything_else'))
