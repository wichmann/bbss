
"""
bbss - BBS Student Management

Init script for bbss package.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""


import random
import sys


# init random number generator for password generation
random.seed()


# check whether the correct system encoding is given
if sys.getfilesystemencoding().lower() not in ('utf-8'):
    raise Exception("BBSS requires a UTF-8 locale.")
