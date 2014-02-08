
"""
bbss - BBS Student Management

Data storage classes and helper functions for altering stored data, e.g.
removing illegal characters in names or replacing class names by LUT.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import random
import logging

from bbss import config
from bbss import ad


logger = logging.getLogger('bbss.data')


class Student(object):
    def __init__(self, surname, firstname, classname, birthday):
        self.surname = surname
        self.firstname = firstname
        self.classname = classname
        self.birthday = birthday

    def __str__(self):
        return "<{0} {1} from {2}>".format(self.firstname,
                                           self.surname,
                                           self.classname)

    def get_class_name(self):
        return replace_class_name(self.classname)

    def get_class_determinator(self):
        return replace_class_name(self.classname).rstrip('1234567890')

    def get_department(self):
        for department in config.department_map:
            if self.get_class_determinator() in department:
                return config.department_map[department]
        return ''

    def generateUserID(self):
        """generates a user id for this student"""
        s = '%s.%s%s' % (self.get_class_name(), self.surname[0:4].upper(),
                         self.firstname[0:4].upper())
        return s

    def generatePassword(self):
        # password generation:
        #http://stackoverflow.com/questions/3854692/generate-password-in-python
        # import string
        # from random import sample, choice
        # chars = string.letters + string.digits
        # length = 8
        # return ''.join(sample(chars,length))
        return 'A##' + str(random.randint(1000, 9999))

    def generateOU(self):
        return ad.generateOU(self.get_class_name(),
                             self.get_class_determinator(),
                             self.get_department())


def replace_illegal_characters(string):
    """Replaces illegal characters from a given string with values from char
       map (see bbss.config)."""
    characters = list(string)
    return ''.join([config.char_map[char] if char in config.char_map
                   else char for char in characters])


def replace_class_name(string):
    """replace class names that have to be changed for generating user names"""
    return config.class_map[string] if string in config.class_map else string


class ChangeSet(object):
    def __init__(self):
        self.students_added = []
        self.students_removed = []
        self.students_changed = []

    def temp(self):
        pass
