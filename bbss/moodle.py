
"""
bbss - BBS Student Management

Exports student data for Moodle server.

Created on Tue Jun  20 11:22:56 2017

@author: Christian Wichmann
"""


import os
import csv
import logging
from itertools import chain

from bbss import data


__all__ = ['export_data']


logger = logging.getLogger('bbss.moodle')


def export_data(output_file, change_set, replace_illegal_characters=False):
    # class list file not necessary, because cohorts will be created by uploading
    # user list (source: https://docs.moodle.org/33/en/Cohorts#Uploading_users_to_a_cohort)
    # _write_class_list_file(output_file, change_set)
    _write_student_list_file(output_file, change_set, replace_illegal_characters)
    _write_cohorts_file(output_file, change_set)


def _write_class_list_file(output_file, change_set):
    """
    Writes a file containing all data to import new classes into Moodle. New
    classes will be represented by a global group each, containing all students
    of that class. Groups for classes that no longer exist, will not be deleted
    automatically.

    :param output_file: file name to write class list to
    :param change_set: object representing all changes between given imports

    TODO: Check how to delete no longer needed classes automatically.

    Export globale gruppe Datei:
    name    idnumber   description
    hl      HL2
    """
    output_file += '.classes'
    if os.path.exists(output_file):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('name', 'idnumber', 'description'))
        for c in change_set.classes_added:
            output_file_writer.writerow((c, c, ''))


def _write_cohorts_file(output_file, change_set):
    """
    Writes a file containing all assignments between students and cohorts.

    :param output_file: file name to write cohorts list to
    :param change_set: object representing all changes between given imports

    Export globale gruppe Datei:
    username,cohort1,cohort2
    student1,nursing,2016class
    student2,nursing,2014class
    student3,nursing,2014class
    """
    output_file = os.path.splitext(output_file)
    output_file_cohorts = '{}.cohorts{}'.format(*output_file)
    if os.path.exists(output_file_cohorts):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file_cohorts, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('username', 'cohort1', 'cohort2', 'cohort3', 'cohort4',
                                     'cohort5', 'cohort6', 'cohort7', 'cohort8', 'cohort9',
                                     'cohort10', 'cohort11', 'cohort12', 'cohort13', 'cohort14'))
        for student in sorted(chain(change_set.students_added, change_set.students_changed)):
            if student.courses:
                c = student.courses.split(',')
                course_names = ['Kurs-{}'.format(x.lower()) for x in c] + [''] * (14 - len(c))
                output_file_writer.writerow((student.user_id, *course_names))


def _write_student_list_file(output_file, change_set, replace_illegal_characters):
    """
    Writes a file containing all data to import students into Moodle. All new
    students will be included. Each student no longer in the database, will be
    included in the file with the "deleted" parameter set to "1".

    :param output_file: file name to write student list to
    :param change_set: object representing all changes between given imports
    :param replace_illegal_characters: whether to replace illegal (non-ASCII)
                                       characters in class and student names

    File format for importing users into Moodle:
    username,   password,   firstname, lastname, email, cohort1,   sysrole1,                        deleted
    ifa51.jone, verysecret, Tom,       Jones,    ,      IFA51,     Teilnehmer/in,                   0
    fse51.gege, geheim,     Hans,      Meyer,    ,      FSE61,     Teilnehmer/in,                   1
    wich,       fdlkj,      Christian, Wichmann, ,      Kollegium, Trainer/in und Kursersteller/in, 0

    Other possible fields are: role1 (for students: 5), oldusername, deleted, suspended

    Possible roles in the Moodle system including their german names:
    Manager/in	                          manager
    Kursersteller/in                      coursecreator
    Trainer/in                            editingteacher
    Trainer/in ohne Bearbeitungsrecht	  teacher
    Teilnehmer/in                         student
    """
    output_file = os.path.splitext(output_file)
    output_file_added_students = '{}.added{}'.format(*output_file)
    output_file_removed_students = '{}.removed{}'.format(*output_file)
    output_file_log = '{}.log{}'.format(*output_file)
    if os.path.exists(output_file_added_students) or os.path.exists(output_file_removed_students) or os.path.exists(output_file_log):
        logger.warning('Output file already exists, will be overwritten...')
    # create empty log file
    open(output_file_log, 'w').close()
    # export file with all added students
    with open(output_file_added_students, 'w', newline='', encoding='utf8') as csvfile:
        count = 0
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('cohort1', 'lastname', 'firstname', 'username',
                                     'password', 'email', 'deleted'))
        for student in sorted(chain(change_set.students_added, change_set.students_changed)):
            _write_student(student, output_file_writer, replace_illegal_characters, False)
            count += 1
        logger.debug('{0} students (added) exported to Moodle file format.'.format(count))
    # export file with all removed students
    with open(output_file_removed_students, 'w', newline='', encoding='utf8') as csvfile:
        count = 0
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('cohort1', 'lastname', 'firstname', 'username',
                                     'password', 'email', 'deleted'))
        for student in sorted(change_set.students_removed):
            # set delete column for removed students
            _write_student(student, output_file_writer, replace_illegal_characters, True)
            count += 1
        logger.debug('{0} students (removed) exported to Moodle file format.'.format(count))


def _write_student(student, output_file_writer, replace_illegal_characters, deleted):
    """
    Writes the data of a single student to CSV file. The "deleted" parameter defines
    whether to delete the student in Moodle or to add it to the system.

    :param student: object representing a single students data
    :param output_file_writer: CSV file to write to
    :param replace_illegal_characters: whether to replace illegal (non-ASCII)
                                       characters in class and student names
    :param deleted: whether to delete the student in Moodle
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
    # construct fake mail address if no mail address is saved in database
    mail_address = student.email if student.email else '{}@example.com'.format(user_id)
    output_file_writer.writerow((class_of_student,
                                 surname_of_student,
                                 firstname_of_student,
                                 # username has to be lowercase only!
                                 user_id,
                                 student.generate_password(),
                                 mail_address,
                                 '1' if deleted else '0'))
