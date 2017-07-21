
"""
bbss - BBS Student Management

Exports student data for use with WebUntis.

Created on Fri Jul 21 11:26:47 2017

@author: Christian Wichmann
"""


import csv
import os
import logging
import datetime

from bbss import data


__all__ = ['export_data']


logger = logging.getLogger('bbss.webuntis')


def export_data(output_file, change_set):
    list_of_passwords = _write_class_list_file(output_file, change_set)
    print_password_list(list_of_passwords)


def _write_class_list_file(output_file, change_set):
    """
    Writes a file containing all data to import new classes into WebUntis. For
    each new class between the given imports, a new user will be created.
    Classes that are no longer in the database will not be deleted automatically.

    :param output_file: file name to write class list to
    :param change_set: object representing all changes between given imports
    """
    list_of_passwords = {}
    if os.path.exists(output_file):
        logger.warn('Output file already exists, will be overwritten...')
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=',')
        output_file_writer.writerow(('Klassenname', 'Kurzname', 'Passwort', 'Personenrolle', 'Benutzergruppe'))
        for c in change_set.classes_added:
            new_password = data.generate_good_password()
            list_of_passwords[c] = new_password
            output_file_writer.writerow((c, c, new_password, 'Klasse', 'Klassen'))
    return list_of_passwords


def print_password_list(list_of_passwords):
    print('-----------------')
    for k, v in list_of_passwords.items():
        print(k, v)
