
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
from collections import namedtuple

from bbss import config
from bbss import ad


#
# Alternatives for generating better passwords: 
# pronounceable passwords in Python: https://www.ibisc.univ-evry.fr/~fpommereau/blog/2015-05-07-generating-pronounceable-passwords-in-python.html
# and: https://exyr.org/2011/random-pronounceable-passwords/
#


logger = logging.getLogger('bbss.data')


PASSWORD_LENGTH = 8


@total_ordering
class Student(object):
    """
    Holds all information of a single student.

    If an user_id and password has already been assigned to a student this
    data has to be stored. Otherwise these data has to be generated when
    it is first needed, e.g. for exporting or storing in the database.
    """
    def __init__(self, surname, firstname, classname, birthday):
        self.surname = surname
        self.firstname = firstname
        self.classname = classname
        self.birthday = birthday
        self.email = ''
        # store GUID for student ALWAYS as string, because it is easier to handle
        self.guid = ''
        self.user_id = None
        self.password = None

    def __str__(self):
        return "<{0} {1} from {2}>".format(self.firstname,
                                           self.surname,
                                           self.classname)

    def __eq__(self, other):
        if other == None:
            return False
        return ((self.surname, self.firstname, self.birthday) ==
                (other.surname, other.firstname, other.birthday))

    def __lt__(self, other):
        # FIXME Check if different implementations of __eq__ and __lt__ result
        #       in problematic effects when sorting lists of students!
        return ((self.classname, self.surname, self.firstname, self.birthday) <
                (other.classname, other.surname, other.firstname, other.birthday))

    def get_class_name_for_username(self):
        """Returns class name after replacement map has been applied. All
        relevant replacements can be found in config module."""
        return replace_class_name(self.classname)

    def get_class_name_for_class_id(self):
        """Returns class name for use in the class identifier in output formats.
        Some replacements from config module are applied, but NOT ALL of
        them!"""
        exceptions = ['BGT11A', 'BGT11B', 'BGT11C', 'BGT11D', 'BGT12', 'BGT13',
                      'TG11A', 'TG11B', 'TG11C', 'TG11D', 'TG12', 'TG13']
        return replace_class_name(self.classname, exceptions)

    def get_class_determinator(self):
        return replace_class_name(self.classname).rstrip('1234567890')

    def get_department(self):
        for department in config.department_map:
            if self.get_class_determinator() in department:
                return config.department_map[department]
        return ''

    def generate_user_id(self, regenerate=False):
        """
        Generates a user id for a student if it does not exist already.
        Otherwise the existing user id is returned! The default user id is
        returned as all caps string.
        
        Currently the existing user id is NEVER replaced even when an existing
        student is in the database and her class name changed! The database
        functions call this method to get the user id. Changing user ids when
        classes are changed, could be handled here?!
        """
        if not self.user_id or regenerate:
            self.user_id = '%s.%s%s' % (self.get_class_name_for_username(),
                                        replace_illegal_characters(self.surname)[0:4].upper(),
                                        replace_illegal_characters(self.firstname)[0:4].upper())
        return self.user_id

    def generate_password(self, regenerate=False):
        """Generates a password for a student if it does not exist already.
        Otherwise the existing password is returned!
        """
        if not self.password or regenerate:
            self.password = generate_good_readable_password()
        return self.password

    def generate_ou(self):
        # TODO move to bbss.ad
        return ad.generateOU(self.get_class_name_for_username(),
                             self.get_class_determinator(),
                             self.get_department())


def generate_simple_password():
    """Deprecated function for generating simple password by using a four digit
    number and concatenating it to a fixed string."""
    return 'A##' + str(random.randint(1000, 9999))


def generate_random_password():
    """
    Generate a random password for a given length including all letters and
    digits. To generate unpredictable passwords, the SystemRandom class from
    the random module is used!

    See also: http://stackoverflow.com/questions/3854692/generate-password-in-python

    :return: string containing random password
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().sample(chars, PASSWORD_LENGTH))


def generate_good_password():
    """
    Generate a random password for a given length including all letters and
    digits. This password contains at least one lower case letter, one upper
    case letter and one digit. To generate unpredictable passwords, the
    SystemRandom class from the random module is used!

    :return: string containing random password of good quality
    """
    chars = string.ascii_letters + string.digits
    # fill up with at least one uppercase, one lowercase and one digit
    password = []
    password += random.SystemRandom().choice(string.ascii_uppercase)
    password += random.SystemRandom().choice(string.ascii_lowercase)
    password += random.SystemRandom().choice(string.digits)
    # fill password up with more characters
    password += [random.SystemRandom().choice(chars) for _ in range(PASSWORD_LENGTH-3)]
    # shuffle characters of password string
    random.shuffle(password)
    logger.debug('New password generated: ' + ''.join(password))
    return ''.join(password)


def generate_good_readable_password():
    """
    Generate a random password for a given length including all letters and
    digits. This password contains at least one lower case letter, one upper
    case letter and one digit. To generate unpredictable passwords, the
    SystemRandom class from the random module is used! All ambiguous characters
    are exempt from passwords.

    Source: https://stackoverflow.com/questions/55556/characters-to-avoid-in-automatically-generated-passwords
   
    :return: string containing random password of good quality
    """
    password = []
    # define possible characters for use in passwords (source: https://www.grc.com/ppp.htm)
    uppercase = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    lowercase = 'abcdefghijkmnopqrstuvwxyz'
    digits = '23456789'
    chars = uppercase + lowercase + digits
    # fill up with at least one uppercase, one lowercase and one digit
    password += random.SystemRandom().choice(uppercase)
    password += random.SystemRandom().choice(lowercase)
    password += random.SystemRandom().choice(digits)
    # fill password up with more characters
    password += [random.SystemRandom().choice(chars) for _ in range(PASSWORD_LENGTH-3)]
    # shuffle characters of password string
    random.shuffle(password)
    logger.debug('New password generated: ' + ''.join(password))
    return ''.join(password)


def replace_illegal_characters(string):
    """Replaces illegal characters from a given string with values from char
       map. (See bbss.config)"""
    characters = list(string)
    return ''.join([config.char_map[char] if char in config.char_map
                   else char for char in characters])


def replace_class_name(old_class_name, exceptions=list()):
    """Replaces class names that have to be changed for generating user
       names. (See bbss.config)"""
    new_class_name = old_class_name
    for old, new in config.class_map.items():
        if old not in exceptions:
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


def verify_mail_address(mail_address):
    """
    Verifies whether a given mail address is a legal value. The imported data often
    contains words or abbreviations that were given in the PDF form filled by the
    company of the student.
    """
    mail_address = mail_address.strip().lower()
    # check whether given string is in blacklist
    if mail_address in config.mail_address_blacklist:
        logger.debug('Illegal mail address found: {}'.format(mail_address))
        return ''
    # check whether the string contains only one charater like ['-', 'x', '.', '-', '?', '/']
    if len(set(mail_address)) == 1:
        logger.debug('Illegal mail address found: {}'.format(mail_address))
        return ''
    # ceck whether a @ character is present
    if '@' not in mail_address:
        logger.debug('Illegal mail address found: {}'.format(mail_address))
        return ''
    # TODO: Check whether it is necessary to check address with Pythons email.utils.parseaddr().
    return mail_address


ChangeSetStatistics = namedtuple('ChangeSetStatistics', 'added changed removed')

class ChangeSet(object):
    """
    Defines all changes between two imports of student data.

    After importing student data it is stored into the database. For some uses
    it is necessary to get all changed students. That includes all added,
    removed and changed student entities. This diff is stored by a ChangeSet
    and can be used for exporting this data into various formats.
    """
    def __init__(self):
        self.students_added = []
        self.students_removed = []
        self.students_changed = []
        self.classes_added = []
        self.classes_removed = []

    def get_statistics(self):
        return ChangeSetStatistics(len(self.students_added), len(self.students_changed), len(self.students_removed))
