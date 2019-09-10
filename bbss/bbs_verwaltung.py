
"""
bbss - BBS Student Management

Imports and exports student data from CSV files created by BBS-Verwaltung.

Created on Wed Jan 23 12:59:34 2019

@author: Christian Wichmann
"""


import csv
import uuid
import logging
import datetime

from bbss import data


__all__ = ['import_data']


logger = logging.getLogger('bbss.bbs_verwaltung')


def import_data(import_file):
    student_count = 0
    student_list = []
	# open CSV file with strange encoding because otherwise BOM markers show up
    with open(import_file, 'r', encoding='utf-8-sig') as csvfile:
        student_file_reader = csv.reader(csvfile, delimiter=';')
        for row in student_file_reader:
            student_count += _read_student(row, student_list)
        logger.info('{} students imported.'.format(student_count))
        return student_list


def _read_student(row, student_list):
    """Reads a single student (her/his data) from a row of a csv file.
	
	Columns:
	GUID, E-Mailadresse, Username im AD, Nachname, Vorname, Klasse, Kurse,
    Geb. Datum, Initial-Passwort, löschen, Neu, LK=-1/SuS=0, Gruppen-
    zugehörigkeit z.B. für E-Mail
	"""
    student_count = 0
    try:
        # parse GUID as validation, although it is stored as string in the database
        guid = uuid.UUID(str(row[0]))
    except ValueError:
        # create new random UUID if value from file could not be parsed
        logger.error('Could not parse UUID: ', str(row[0]))
        guid = uuid.uuid4()
    # assign all values from row
    mail_adress = row[1]
    username = row[2]
    surname = row[3]
    firstname = row[4]
    classname = row[5]
    courses = row[6]
    birthday = row[7]
    initial_password = row[8]
    student_was_deleted = row[9]     # deleted = -1 / else = 0, set always after student was moved to "Abgänger"
    is_new_user = row[10]            # new = -1 / else = 0, only set once after student was added
    is_teacher_or_student = row[11]  # teacher = -1 / student = 0
    group_memberships = row[12]
    # check if student was deleted in BBS-Verwaltung and should therefore not be imported
    if student_was_deleted == '-1':
        logger.debug('Deleted student not imported: {0} {1} ({2})'.format(firstname, surname, classname))
        return student_count
    # check if student or class is blacklisted
    message = 'Student ({0} {1}) not imported because class ({2}) is blacklisted.'
    if data.is_class_blacklisted(classname):
        logger.debug(message.format(firstname, surname, classname))
        return student_count
    if classname[:2] == 'ZZ':
        logger.debug(message.format(firstname, surname, classname))
        return student_count
    # check whether a classname was given in the import file
    if not classname:
        logger.debug(message.format(firstname, surname, classname))
        return student_count
    # check if students name ends with a underscore, because this is an
    # entry for a student that participates in two classes at the same time
    if surname[-1:] == '_':
        return student_count
	# skip teacher user 
    if is_teacher_or_student == -1:
        return student_count
    # convert date of birth
    try:
        birthday = datetime.datetime.strptime(birthday, '%d.%m.%Y').date()
        new_student = data.Student(surname, firstname, classname, birthday)
        # include mail address and GUID
        new_student.email = data.verify_mail_address(mail_adress)
        new_student.guid = str(guid)
        new_student.is_new = (is_new_user == '-1')
        new_student.was_deleted = (student_was_deleted == '-1')
        # append new student to list
        student_list.append(new_student)
        student_count = 1
    except:
        logger.warn('Could not import student because data not valid.')
    return student_count

