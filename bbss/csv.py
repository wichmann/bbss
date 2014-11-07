
"""
bbss - BBS Student Management

Imports and exports student data from csv files.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""


import csv
import os
import logging
import datetime

from bbss import data


__all__ = ['import_data', 'export_data']


logger = logging.getLogger('bbss.csv')


### correlation between columns in the csv file and their attributes
column_map = {'surname': 0,
              'firstname': 0,
              'classname': 0,
              'birthday': 0}


def import_data(import_file):
    student_count = 0
    student_list = []
    with open(import_file, 'r', newline='', encoding='utf8') as csvfile:
        # TODO Set dialect for csv.reader?
        student_file_reader = csv.reader(csvfile)
        # find columns from file
        for column, name in enumerate(next(student_file_reader)):
            if name == 'KL_NAME':
                column_map['classname'] = column
            elif name == 'NNAME':
                column_map['surname'] = column
            elif name == 'VNAME':
                column_map['firstname'] = column
            elif name == 'GEBDAT':
                column_map['birthday'] = column

        for row in student_file_reader:
            student_count += _read_student(row, student_list)
        logger.info('%s student imported.' % student_count)
        return student_list


def _read_student(row, student_list):
    """Reads a single student (her/his data) from a row of a csv file."""
    student_counts = 0
    class_of_student = row[column_map['classname']]
    name_of_student = row[column_map['surname']]
    firstname_of_student = row[column_map['firstname']]
    birthday_of_student = row[column_map['birthday']]
    # check if student or class is blacklisted
    message = 'Student ({0} {1}) not imported because class ({2}) is blacklisted.'
    if data.is_class_blacklisted(class_of_student):
        logger.debug(message.format(firstname_of_student, name_of_student,
                                    class_of_student))
        return student_counts
    if class_of_student[:2] == 'ZZ':
        logger.debug(message.format(firstname_of_student, name_of_student,
                                    class_of_student))
        return student_counts
    if name_of_student[-1:] == '_':
        return student_counts
    # convert date of birth
    try:
        birthday_of_student = datetime.datetime.strptime(
            birthday_of_student, '%d.%m.%Y').date()
        student_list.append(data.Student(name_of_student,
                                         firstname_of_student,
                                         class_of_student,
                                         birthday_of_student))
        student_counts = 1
    except:
        logger.warn('Could not import student because data not valid.')
    return student_counts


def export_data(output_file, change_set, replace_illegal_characters=True):
    if os.path.exists(output_file):
        logger.warn('Output file already exists, will be overwritten...')
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Class', 'Name', 'Firstname', 'UserID',
                                     'Password'))
        for student in sorted(change_set.students_added):
            _write_student(student, output_file_writer,
                           replace_illegal_characters)


def _write_student(student, output_file_writer, replace_illegal_characters):
    """Writes a single student (her/his data) to file writer of csv file."""
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
                           (firstname_of_student,
                            surname_of_student,
                            class_of_student))
    # output student data for change set into file
    output_file_writer.writerow((class_of_student,
                                 surname_of_student,
                                 firstname_of_student,
                                 student.generate_user_id(),
                                 student.generate_password()))
