
"""
bbss - BBS Student Management

Exports student data for LabSoft Classroom Manager.

Created on Fri Jan  05 09:57:22 2018

@author: Christian Wichmann
"""


import os
import csv
import logging
from itertools import chain

from bbss import data


__all__ = ['export_data']


logger = logging.getLogger('bbss.labsoft')


CLASSES_WHITE_LIST = ('KFZ', 'KKB', 'KBK', 'KZF', 'KZM')


def export_data(output_file, change_set, replace_illegal_characters=False):
    _write_student_list_file(output_file, change_set, replace_illegal_characters)


def _write_student_list_file(output_file, change_set, replace_illegal_characters):
    """
    Writes a file containing all data to import students into LabSoft Classroom
    Manager. The student are filtered by class and only classes given in the
    variable CLASSES_WHITE_LIST are included. Students removed from the database
    will be ignored.

    :param output_file: file name to write student list to
    :param change_set: object representing all changes between given imports
    :param replace_illegal_characters: whether to replace illegal (non-ASCII)
                                       characters in class and student names
    """
    if os.path.exists(output_file):
        logger.warn('Output file already exists, will be overwritten...')
    # export file with all added and changed students
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        count = 0
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Login', 'FirstName', 'LastName', 'MemberOf'))
        for student in sorted(chain(change_set.students_added, change_set.students_changed)):
            if any([student.classname.startswith(c) for c in CLASSES_WHITE_LIST]):
                _write_student(student, output_file_writer, replace_illegal_characters)
                count += 1
        logger.debug('{0} students (added) exported to Moodle file format.'.format(count))


def _write_student(student, output_file_writer, replace_illegal_characters):
    """
    Writes the data of a single student to CSV file.
    
    :param student: object representing a single students data
    :param output_file_writer: CSV file to write to
    :param replace_illegal_characters: whether to replace illegal (non-ASCII)
                                       characters in class and student names
    """
    # get data from change set
    class_of_student = student.get_class_name_for_class_id()
    surname_of_student = student.surname
    firstname_of_student = student.firstname
    # replace illegal characters if needed
    if replace_illegal_characters:
        class_of_student, surname_of_student, firstname_of_student =\
            map(data.replace_illegal_characters,
                (class_of_student, surname_of_student,
                 firstname_of_student))
        # check for non ascii characters in string
        try:
            class_of_student.encode('ascii')
            surname_of_student.encode('ascii')
            firstname_of_student.encode('ascii')
        except UnicodeEncodeError:
            logger.warning('Non ascii characters in %s %s in %s' %
                           (firstname_of_student, surname_of_student, class_of_student))
    # output student data for change set into file
    user_id = student.generate_user_id().lower()
    output_file_writer.writerow((user_id, firstname_of_student, surname_of_student, class_of_student))
