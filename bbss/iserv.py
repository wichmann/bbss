
"""
bbss - BBS Student Management

Exports student data for iServ server.

Created on Mon Jun  22 10:47:46 2026

@author: Christian Wichmann
"""


import csv
import logging
from datetime import datetime


__all__ = ['export_data']


logger = logging.getLogger('bbss.iserv')


def export_data(output_file, change_set):
    _write_student_list_file(output_file, change_set)


def _write_student_list_file(output_file, change_set):
    """
    Writes a file containing all data to import students into iServ. All
    students will be included. Each student no longer in the database, will
    not be included, so iServ can delete that user.

    :param output_file: file name to write student list to
    :param change_set: object representing all changes between given imports

    File format for importing users into iServ:
    Import-ID;Vorname;Nachname;Klasse/Information;Account;Passwort;Email;Geburtsdatum;Gruppen
    0075098C-A904-4F48-B6E8-29802C45A0AB;Tom;Jones;IFA51;tom.jones;verysecret;tommy@jones.com;01.02.1999;""
    0075098C-A904-4F48-B6E8-39802C45A0EC;Hans;Meyer;TG11B;hans.meyer;geheim;hand@gmail.com;05.05.2013;"Kurs En 1;AG Handarbeit"
    0075098C-A904-4F48-B6E8-49802C9820ED;Christian;Wichmann;WICHCHRI;christian.wichmann;12345678;wichmann@bbs-os-brinkstr.de;09.09.1980;"Kollegium"
    """
    # export file with all added students
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        count = 0
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Import-ID', 'Vorname', 'Nachname', 'Klasse/Information',
                                     'Account', 'Passwort', 'Email', 'Geburtsdatum', 'Gruppen'))
        for student in sorted(change_set.students_added)[::10]:
            _write_student(student, output_file_writer)
            count += 1
        logger.debug('{0} students (added) exported to Moodle file format.'.format(count))


def _write_student(student, output_file_writer):
    """
    Writes the data of a single student to CSV file.

    :param student: object representing a single students data
    :param output_file_writer: CSV file to write to
    """
    # get data from change set
    mail_address = student.email if student.email else '{}@example.com'.format(student.get_initial_username())
    birthday = datetime.strptime(student.birthday, '%Y-%m-%d').strftime('%d.%m.%Y')
    output_file_writer.writerow((student.guid, student.firstname, student.surname, student.classname,
                                 student.get_initial_username(), student.get_initial_password(),
                                 mail_address, birthday, student.courses))
