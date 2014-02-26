
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
    student_file_reader = csv.reader(open(import_file, 'r'))
    # TODO Set dialect for csv.reader?

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
        class_of_student = row[column_map['classname']]
        name_of_student = row[column_map['surname']]
        firstname_of_student = row[column_map['firstname']]
        birthday_of_student = row[column_map['birthday']]
        # check if student or class is blacklisted
        if data.is_class_blacklisted(class_of_student):
            logger.debug('Student ({0} {1}) not imported because class ({2}) is blacklisted.'
                         .format(firstname_of_student, name_of_student, class_of_student))
            continue
        if class_of_student[:2] == 'ZZ':
            logger.debug('Student ({0} {1}) not imported because class ({2}) is blacklisted.'
                         .format(firstname_of_student, name_of_student, class_of_student))
            continue
        if name_of_student[-1:] == '_':
            continue
        # convert date of birth
        birthday_of_student = datetime.datetime.strptime(birthday_of_student,
                                                         '%d.%m.%Y').date()
        student_list.append(data.Student(name_of_student,
                                         firstname_of_student,
                                         class_of_student,
                                         birthday_of_student))
        student_count += 1
    logger.info('%s student imported.' % student_count)
    return student_list


def export_data(output_file, change_set, replace_illegal_characters=True):
    if os.path.exists(output_file):
        logger.warn('Output file already exists, will be overwritten...')
    output_file_writer = csv.writer(open(output_file, 'w'), delimiter=';')
    output_file_writer.writerow(('Class', 'Name', 'Firstname', 'UserID',
                                 'Password', 'OU'))
    for student in change_set.students_added:
        # get data from change set
        class_of_student = student.get_class_name()
        surname_of_student = student.surname
        firstname_of_student = student.firstname
        # replace illegal characters if needed
        if replace_illegal_characters:
            class_of_student, surname_of_student, firstname_of_student = map(
                data.replace_illegal_characters, (class_of_student,
                                                  surname_of_student,
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
                                     student.generate_password(),
                                     student.generate_ou()))
