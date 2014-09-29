
"""
bbss - BBS Student Management

Data storage classes and helper functions for altering stored data, e.g.
removing illegal characters in names or replacing class names by LUT.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import random
import logging
import string
from functools import total_ordering

from bbss import config
from bbss import ad


logger = logging.getLogger('bbss.data')


PASSWORD_LENGTH = 7
    

@total_ordering
class Student(object):
    """Holds all information of a single student.

    If an user_id and password has already been assigned to a student this
    data has to be stored. Otherwise these data has to be generated when
    it is first needed, e.g. for exporting or storing in the database."""
    def __init__(self, surname, firstname, classname, birthday):
        self.surname = surname
        self.firstname = firstname
        self.classname = classname
        self.birthday = birthday
        self.user_id = None
        self.password = None

    def __str__(self):
        return "<{0} {1} from {2}>".format(self.firstname,
                                           self.surname,
                                           self.classname)

    def __eq__(self, other):
        return ((self.surname, self.firstname, self.birthday) ==
                (other.surname, other.firstname, other.birthday))

    def __lt__(self, other):
        # FIXME Check if different implementations of __eq__ and __lt__ result
        # in problematic effects when sorting lists of students!
        return ((self.classname, self.surname, self.firstname, self.birthday) <
                (other.classname, other.surname, other.firstname, other.birthday))

    def get_class_name(self):
        return replace_class_name(self.classname)

    def get_class_determinator(self):
        return replace_class_name(self.classname).rstrip('1234567890')

    def get_department(self):
        for department in config.department_map:
            if self.get_class_determinator() in department:
                return config.department_map[department]
        return ''

    def generate_user_id(self):
        """Generates a user id for a student if it does not exist already.
        Otherwise the existing user id is returned!
        
        Currently the existing user id is NEVER replaced even when an existing
        student is in the database and her class name changed! The database
        functions call this method to get the user id. Changing user ids when
        classes are changed, could be handled here?!"""
        if not self.user_id:
            self.user_id = '%s.%s%s' % (self.get_class_name(),
                                        replace_illegal_characters(self.surname)[0:4].upper(),
                                        replace_illegal_characters(self.firstname)[0:4].upper())
        return self.user_id

    def generate_password(self):
        """Generates a password for a student if it does not exist already.
        Otherwise the existing password is returned!
        """
        if not self.password:
            self.password = generate_good_password()
        return self.password

    def generate_ou(self):
        # TODO move to bbss.ad
        return ad.generateOU(self.get_class_name(),
                             self.get_class_determinator(),
                             self.get_department())


def generate_simple_password():
    """Deprecated function for generating simple passwort by using a four digit
    number and concatenating it to a fixed string."""
    return 'A##' + str(random.randint(1000, 9999))


def generate_random_password():
    # generate a good password
    # http://stackoverflow.com/questions/3854692/generate-password-in-python
    chars = string.ascii_letters + string.digits
    return ''.join(random.sample(chars, PASSWORD_LENGTH))


def generate_good_password():
    # load password with at least one lower case letter, one upper case letter
    # and one digit
    password = []
    password += random.choice(string.ascii_uppercase)
    password += random.choice(string.ascii_lowercase)
    password += random.choice(string.digits)
    # fill password up with more characters
    chars = string.ascii_letters + string.digits
    password += [random.choice(chars) for _ in range(PASSWORD_LENGTH-3)]
    logger.debug('New password generated: ' + ''.join(password))
    return ''.join(password)


def replace_illegal_characters(string):
    """Replaces illegal characters from a given string with values from char
       map. (See bbss.config)"""
    characters = list(string)
    return ''.join([config.char_map[char] if char in config.char_map
                   else char for char in characters])


def replace_class_name(old_class_name):
    """Replaces class names that have to be changed for generating user
       names. (See bbss.config)"""
    new_class_name = old_class_name
    for old, new in config.class_map.items():
        new_class_name = new_class_name.replace(old, new)
    if old_class_name != new_class_name:
        logger.debug("old class: {} -> new class: {}".format(old_class_name,
                                                             new_class_name))
    return new_class_name


def is_class_blacklisted(class_name):
    for blacklisted_class in config.class_blacklist:
            if blacklisted_class in class_name:
                return True
    return False


class ChangeSet(object):
    """Defines all changes between two imports of student data.

    After importing student data it is stored into the database. For some uses
    it is necessary to get all changed students. That includes all added,
    removed and changed student entities. This diff is stored by a ChangeSet
    and can be used for exporting this data into various formats."""
    def __init__(self):
        self.students_added = []
        self.students_removed = []
        self.students_changed = []

    def temp(self):
        pass
