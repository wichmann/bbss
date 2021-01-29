
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


__all__ = ['import_data', 'export_data', 'import_user_list_from_moodle', 'export_differences_list']


logger = logging.getLogger('bbss.csv')


# TODO: Import mail adresses from CSV file like the XLS import does!!!

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
        logger.warning('Could not import student because data not valid.')
    return student_counts


def export_data(output_file, change_set, replace_illegal_characters=True):
    if os.path.exists(output_file):
        logger.warning('Output file already exists, will be overwritten...')
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


def import_user_list_from_moodle(import_file):
    """
    Imports a list of all student from Moodle to allow comparisions for mail address and other fields.

    The list can be generated in Moodle by the user management feature:

    * Website-Administration -> Nutzer/innen -> Nutzerkonten -> Nutzerverwaltung (Bulk)
    * Filterergebnis: Alle verfügbaren -> Button "Alle hinzufügen"
    * Dropdown-Feld "Für ausgewählte Nutzer/innen..." -> "Download" auswählen
    """
    fieldnames = ['id', 'username', 'email', 'firstname', 'lastname', 'idnumber',
                  'institution', 'department', 'phone1', 'phone2', 'city',
                  'url', 'icq', 'skype', 'aim', 'yahoo', 'msn', 'country',
                  'profile_field_dateofbirth', 'profile_field_placeofbirth',
                  'profile_field_gender', 'profile_field_class']
    student_list = []
    with open(import_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', fieldnames=fieldnames)
        for row in reader:
            username = row['username']
            mail_adress = row['email']
            last_name = row['lastname']
            first_name = row['firstname']
            new_student = data.Student(last_name, first_name, '', '')
            # no validation necessary, because Moodle only contains valid mail addresses
            new_student.email = mail_adress
            new_student.user_id = username
            # append new student to list
            student_list.append(new_student)
    return student_list


def export_differences_list(output_file, differences_list):
    """
    Exports a CSV file containing all users with differences in their mail
    addresses between Moodle and BBS-Verwaltung.
    """
    if os.path.exists(output_file):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file, 'w', newline='', encoding='cp1252') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Nachname', 'Vorname', 'Mail in BBS-Verwaltung', 'Mail in Moodle'))
        for c in differences_list:
            output_file_writer.writerow((c[0].surname, c[0].firstname, c[0].email, c[1].email))
