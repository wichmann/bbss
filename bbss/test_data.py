
"""
bbss - BBS Student Management

Unit tests for data storage classes and their helper functions.

Created on Tue Sep 23 15:08:56 2014

@author: Christian Wichmann
"""

import logging
import unittest

from bbss import data


logger = logging.getLogger('bbss.data')


class TestData(unittest.TestCase):

    def setUp(self):
        pass

    def test_generate_good_password(self):
        for i in range(100000):
            # get new random password
            password = data.generate_good_password()
            self.assertEqual(len(password), 7)
            self.assertEqual(any(char.isdigit() for char in password), True)
            self.assertEqual(any(char.islower() for char in password), True)
            self.assertEqual(any(char.isupper() for char in password), True)

    def test_replace_illegal_characters(self):
        pass


if __name__ == '__main__':
    unittest.main()
