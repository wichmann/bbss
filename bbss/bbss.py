
"""
bbss - BBS Student Management

Reads student data from csv files and stores them in a database. Data can be
exported to be used by other systems like AD or RADIUS servers.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""


import csv
import logging
import os

from bbss import config
from bbss import data
from bbss import db


logger = logging.getLogger('bbss.main')


student_list = []
student_database = db.StudentDatabase()

### correlation between columns in the csv file and their attributes
column_map = {'surname': 0,
              'firstname': 0,
              'classname': 0,
              'birthday': 0}


def read_csv_file(input_file):
    """reads a csv file and adds student to list"""
    logger.info('Importing students from file...')
    global student_list
    student_count = 0
    student_file_reader = csv.reader(open(input_file, 'r'))
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
        class_of_student = data.replace_illegal_characters(row[column_map['classname']])
        name_of_student = data.replace_illegal_characters(row[column_map['surname']])
        firstname_of_student = data.replace_illegal_characters(row[column_map['firstname']])
        birthday_of_student = row[column_map['birthday']]
        if class_of_student in config.class_blacklist:
            continue
        if name_of_student[-1:] == '_':
            continue
        try:
            # check for non ascii characters in string
            class_of_student.encode('ascii')
            name_of_student.encode('ascii')
            firstname_of_student.encode('ascii')
            birthday_of_student.encode('ascii')
        except UnicodeEncodeError:
            logger.warning('Non ascii characters in %s %s in %s' % (firstname_of_student, name_of_student, class_of_student))
        student_list.append(data.Student(name_of_student,
                                         firstname_of_student,
                                         class_of_student,
                                         birthday_of_student))
        student_count += 1
    logger.info('%s student imported.' % student_count)
    # check for double entries in student list
    check_for_doubles()


def output_csv_file(output_file):
    """Outputs a csv file with all information for all students for the AD."""
    logger.info('Writing student data to csv file...')
    if os.path.exists(output_file):
        logger.warn('Output file already exists, will be overwritten...')
    output_file_writer = csv.writer(open(output_file, 'w'), delimiter=';')
    output_file_writer.writerow(('Class', 'Name', 'Firstname', 'UserID',
                                 'Password', 'OU'))
    global student_database
    change_set = student_database.generate_changeset()
    for student in change_set.students_added:
        output_file_writer.writerow((student.get_class_name(),
                                     student.surname,
                                     student.firstname,
                                     student.generateUserID(),
                                     student.generatePassword(),
                                     student.generateOU()))
    logger.info('Student list written to file.')


def check_for_doubles():
    """Checks for students with the same generated user name."""
    logger.info('Checking student list for doubles...')
    global student_list
    seen = set()
    for student in student_list:
        if student.generateUserID() in seen:
            logger.warning('Double entry ' + student.generateUserID())
        seen.add(student.generateUserID())


def store_students_db(importfile_name):
    """Stores a new set of student data in student database. The database is
       initialized the first time it is used."""
    global student_database
    student_database.store_students_db(importfile_name, student_list)
    student_database.print_statistics()
