
"""
bbss - BBS Student Management

Reads student data from csv files and stores them in a database. Data can be
exported to be used by other systems like AD or RADIUS servers.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import logging
import os

import bbss.db
import bbss.csv


__all__ = ['read_csv_file', 'output_csv_file',
           'store_students_db', 'clear_database']
__version__ = '0.0.1'


logger = logging.getLogger('bbss.main')


student_list = []
student_database = bbss.db.StudentDatabase()


def read_csv_file(input_file):
    """reads a csv file and adds student to list"""
    logger.info('Importing students from file...')
    global student_list
    student_list = bbss.csv.import_data(input_file)
    _check_for_doubles()


def output_csv_file(output_file, replace_illegal_characters=True):
    """Outputs a csv file with all information for all students for the AD."""
    logger.info('Writing student data to csv file...')
    global student_database
    change_set = student_database.generate_changeset()
    bbss.csv.export_data(output_file, change_set, replace_illegal_characters)
    logger.info('Student list written to file.')


def _check_for_doubles():
    """Checks for students with the same generated user name."""
    logger.info('Checking student list for doubles...')
    global student_list
    seen = set()
    for student in student_list:
        if student.generate_user_id() in seen:
            logger.warning('Double entry ' + student.generateUserID())
        seen.add(student.generate_user_id())


def store_students_db(importfile_name):
    """Stores a new set of student data in student database. The database is
       initialized the first time it is used."""
    global student_database
    student_database.store_students_db(importfile_name, student_list)
    student_database.print_statistics()


def search_student_in_database(search_string):
    return student_database.search_for_student(search_string)


def clear_database():
    os.remove(bbss.db.DB_FILENAME)
