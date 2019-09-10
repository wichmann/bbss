
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
import bbss.pdf
import bbss.radius
import bbss.xls
import bbss.moodle
import bbss.webuntis
import bbss.labsoft
import bbss.bbs_verwaltung


__all__ = ['import_csv_file', 'import_excel_file',
           'import_bbs_verwaltung_csv_file', 'export_csv_file',
           'export_moodle_file', 'export_webuntis_file', 'export_labsoft_file',
           'export_radius_file', 'export_pdf_file', 
           'clear_database', 'store_students_db',
           'search_student_in_database', 'generate_changeset']


logger = logging.getLogger('bbss.main')


student_list = []
student_database = bbss.db.StudentDatabase()


# TODO: Replace seperate functions for different import/export file formats
#       with one function taking the file format as parameter.


def import_csv_file(input_file):
    """Reads a csv file and adds student to list."""
    logger.info('Importing students from file...')
    global student_list
    student_list = bbss.csv.import_data(input_file)
    _check_for_doubles()


def import_bbs_verwaltung_csv_file(input_file):
    """Reads a CVS file from BBS-Verwaltung and adds student to list."""
    logger.info('Importing students from file...')
    global student_list
    student_list = bbss.bbs_verwaltung.import_data(input_file)
    _check_for_doubles()


def import_excel_file(input_file, callback=None):
    """Reads a Microsoft Excel file and adds student to list."""
    logger.info('Importing students from file...')
    global student_list
    student_list = bbss.xls.import_data(input_file, callback)
    _check_for_doubles()


def export_csv_file(output_file, changes, replace_illegal_characters=True):
    """Writes a csv file with student data stored in the database."""
    logger.info('Writing student data to csv file...')
    bbss.csv.export_data(output_file, changes, replace_illegal_characters)
    logger.info('Student list written to file.')


def export_radius_file(output_file, changes, replace_illegal_characters=True):
    """Writes a file for use in FreeRadius server."""
    logger.info('Writing student data to radius file...')
    bbss.radius.export_data(output_file, changes,
                            replace_illegal_characters)
    logger.info('Student list written to file.')


# Changed default policy to not replacing illegal characters anymore [20170105].
def export_moodle_file(output_file, changes, replace_illegal_characters=False):
    """Writes a file for use in Moodle server."""
    logger.info('Writing student data to Moodle file...')
    bbss.moodle.export_data(output_file, changes,
                            replace_illegal_characters)
    logger.info('Student list written to file.')


def export_webuntis_file(output_file, changes):
    """Writes a file for use in WebUntis."""
    logger.info('Writing student data to WebUntis file...')
    bbss.webuntis.export_data(output_file, changes)
    logger.info('Student list written to file.')


def export_labsoft_file(output_file, changes):
    """Writes a file for use in LabSoft Classroom Manager."""
    logger.info('Writing student data to LabSoft Classroom Manager file...')
    bbss.labsoft.export_data(output_file, changes)
    logger.info('Student list written to file.')


def export_pdf_file(output_file, student_list):
    """Writes a PDF file to be distributed to the students."""
    logger.info('Writing student list to PDF file...')
    bbss.pdf.export_data(output_file, student_list)
    logger.info('Student list written to file.')


def generate_changeset(old_import_id=0, new_import_id=0):
    """Generates a changeset between two given imports."""
    global student_database
    changes = student_database.generate_changeset(old_import_id, new_import_id)
    return changes


def _check_for_doubles():
    """Checks for students with the same generated user name."""
    logger.info('Checking student list for doubles...')
    global student_list
    seen = set()
    for student in student_list:
        if student.generate_user_id() in seen:
            logger.warning('Double entry ' + student.generate_user_id())
        seen.add(student.generate_user_id())


def store_students_db(importfile_name, callback=None):
    """Stores a set of student data in student database.

    The database is initialized the first time it is used. By calling this
    function a newly imported student list will be added to the database.
    In the database the name of the imported file is also stored for future
    reference.
    
    :param importfile_name: name of the file from which the students were
                            imported
    :param callback: Function that is called after each of the students that
                     are imported. First parameter is the current imported
                     student, second parameter is the number of students to be
                     imported.
    """
    global student_database
    student_database.store_students_db(importfile_name, student_list, callback)
    student_database.print_statistics()


def search_student_in_database(search_string):
    return student_database.search_for_student(search_string)


def get_imports_for_student(student):
    """
    Gets a list of the import IDs for all imports that contain the given
    student. The student is identified by her first name, last name and
    birthday.

    :param student: student to find imports for
    :return: list of imports containing the given student
    """
    return student_database.get_imports_for_student(student.firstname, student.surname, student.birthday)


def clear_database():
    """
    Clears database by removing its file from the filesystem.

    All student data is stored in a database file on the filesystem in the
    directory the main application is started. By calilng this function this
    file will be deleted without a additional confirmation!
    """
    try:
        global student_database
        student_database.close_connection()
        os.remove(bbss.db.DB_FILENAME)
        student_database = bbss.db.StudentDatabase()
    except:
        logger.info('No database file found.')


def get_class_history(student_id):
    return student_database.get_class_history(student_id)
