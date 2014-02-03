#! /usr/bin/env python3

#####
# bbss - BBS Student Management
#
# Reads student data from csv files and stores them in a database. Data
# can be exported to be used by other systems like AD or RADIUS servers.
#
# Author: Christian Wichmann
# Date: 2013-09-15
#####


import csv
import random
import argparse
import sqlite3
import datetime
import logging
import logging.handlers
import sys


LDAP_SERVER = 'ldaps://dc.host.com'
USER_BASE = 'ou=Schueler,ou=BBSBS,DC=SN,DC=BBSBS,DC=LOCAL'

student_list = []

### correlation between columns in the csv file and their attributes
column_map = {'surname': 0,
              'firstname': 1,
              'classname': 2}


class Student:
    def __init__(self, surname, firstname, classname):
        self.surname = surname
        self.firstname = firstname
        self.classname = classname
        # TODO get birthday from csv file
        self.birthday = "2013-09-15"

    def get_class_name(self):
        return replace_class_name(self.classname)

    def get_class_determinator(self):
        return replace_class_name(self.classname).rstrip('1234567890')

    def get_department(self):
        for department in config.department_map:
            if self.get_class_determinator() in department:
                return config.department_map[department]
        return ''

    def generateUserID(self):
        """generates a user id for this student"""
        s = '%s.%s%s' % (self.get_class_name(), self.surname[0:4].upper(), self.firstname[0:4].upper())
        return s

    def generatePassword(self):
        # password generation: http://stackoverflow.com/questions/3854692/generate-password-in-python
        # import string
        # from random import sample, choice
        # chars = string.letters + string.digits
        # length = 8
        # return ''.join(sample(chars,length))
        return 'A##' + str(random.randint(1000, 9999))

    def generateOU(self):
        s = 'ou=' + self.get_class_name() + ','
        s += 'ou=' + self.get_class_determinator() + ','
        s += 'ou=' + self.get_department() + ',' + USER_BASE
        return s


def read_csv_file(input_file):
    """reads a csv file and adds student to list"""
    logger.info('Importing student from file...')

    student_count = 0
    student_file_reader = csv.reader(input_file)
    # TODO set dialect for csv.reader?

    # find columns from file
    for column, name in enumerate(next(student_file_reader)):
        if name == 'KL_NAME':
            column_map['classname'] = column
        elif name == 'NNAME':
            column_map['surname'] = column
        elif name == 'VNAME':
            column_map['firstname'] = column

    for row in student_file_reader:
        class_of_student = replace_illegal_characters(row[column_map['classname']])
        name_of_student = replace_illegal_characters(row[column_map['surname']])
        firstname_of_student = replace_illegal_characters(row[column_map['firstname']])
        if class_of_student in config.class_blacklist:
            continue
        if name_of_student[-1:] == '_':
            continue
        try:
            # check for non ascii characters in string
            class_of_student.encode('ascii')
            name_of_student.encode('ascii')
            firstname_of_student.encode('ascii')
        except UnicodeEncodeError:
            logger.warning('Non ascii characters in %s %s in %s' % (firstname_of_student, name_of_student, class_of_student))
        student_list.append(Student(name_of_student,
                                    firstname_of_student,
                                    class_of_student))
        student_count += 1
    logger.info('%s student imported.' % student_count)


def replace_illegal_characters(string):
    """replace illegal characters from a given string with values from char map"""
    characters = list(string)
    return ''.join([config.char_map[char] if char in config.char_map else char for char in characters])


def replace_class_name(string):
    """replace class names that have to be changed for generating user names"""
    if not options.dontReplaceClassNames:
        return config.class_map[string] if string in config.class_map else string
    else:
        return string


def output_csv_file(output_file):
    """outputs a csv file with all information for all students for the AD"""
    logger.info('Writing student data to csv file...')
    output_file_writer = csv.writer(output_file, delimiter=';')
    output_file_writer.writerow(('Class', 'Name', 'Firstname', 'UserID', 'Password', 'OU'))
    for student in student_list:
        output_file_writer.writerow((student.get_class_name(),
                                     student.surname,
                                     student.firstname,
                                     student.generateUserID(),
                                     student.generatePassword(),
                                     student.generateOU()))
    logger.info('Student list written to file.')


def check_for_doubles():
    """checks for students with the same generated user name"""
    logger.info('Checking student list for doubles...')

    seen = set()
    for student in student_list:
        if student.generateUserID() in seen:
            logger.warning('Double entry ' + student.generateUserID())
        seen.add(student.generateUserID())


def store_students_db():
    """storing student data into database"""
    logger.info('Storing student data into database...')

    # connecting to database
    db_file = 'students.db'
    conn = sqlite3.connect(db_file)
    # change the row factory to use Row to allow access via column name
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # create tables if they not already exist
    cur.execute("CREATE TABLE IF NOT EXISTS Imports(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, date DATE NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS Students(id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT NOT NULL, firstname TEXT NOT NULL, classname TEXT NOT NULL, birthday DATE NOT NULL)")
    cur.execute("CREATE TABLE IF NOT EXISTS StudentsInImports(student_id INT NOT NULL, import_id INT NOT NULL, FOREIGN KEY(student_id) REFERENCES Students(id), FOREIGN KEY(import_id) REFERENCES Imports(id))")
    conn.commit()

    # storing new data in database
    cur.execute("INSERT INTO Imports VALUES(NULL,?,?)", (options.filename_import.name, datetime.date.today()))
    import_id = cur.lastrowid
    conn.commit()

    # storing all students in database
    for student in student_list:
        # check if student is already in database
        cur.execute('SELECT * FROM Students WHERE surname=? AND firstname=? AND birthday=?', (student.surname, student.firstname, student.birthday))
        if not cur.fetchone():
            # insert student in database
            cur.execute('INSERT INTO Students VALUES (NULL,?,?,?,?)', (student.surname, student.firstname, student.classname, student.birthday))
            # insert connection between new student and this import
            student_id = cur.lastrowid
            cur.execute('INSERT INTO StudentsInImports VALUES (?,?)', (student_id, import_id))
        else:
            # change already stored student
            cur.execute('UPDATE Students SET classname=? WHERE surname=? AND firstname=? AND birthday=?', (student.classname, student.surname, student.firstname, student.birthday))
            cur.execute('SELECT * FROM Students WHERE surname=? AND firstname=? AND birthday=?',(student.surname, student.firstname, student.birthday))
            data = cur.fetchone()
            student_id = data[0]
            cur.execute('INSERT INTO StudentsInImports VALUES (?,?)', (student_id, import_id))
    conn.commit()

    # get statistics
    cur.execute('SELECT MAX(id) FROM Imports')
    data = cur.fetchone()
    last_import_id = data['max(id)']
    cur.execute("""SELECT import_id, COUNT(*)
                   FROM (
                SELECT student_id, COUNT(import_id) as cd, import_id
             FROM StudentsInImports
             WHERE import_id = %s OR import_id = %s
             GROUP BY student_id
           )
           WHERE cd = 1
           GROUP BY import_id
           ORDER BY import_id;""" % (last_import_id, last_import_id - 1))
    data = cur.fetchall()
    for element in list(data):
        if element[0] == last_import_id:
            logger.info('%s students added.' % element['count(*)'])
        if element[0] == last_import_id - 1:
            logger.info('%s students removed.' % element['count(*)'])

    # get student count
    cur.execute('SELECT COUNT(*) FROM Students')
    data = cur.fetchone()
    logger.info('%s students currently stored in database.' % data['count(*)'])
    conn.close()


def setup_ad():
    """Set all user accounts for students in AD."""
    logger.info('Setting up ad...')
    logger.info('AD set up.')


def parse_command_line():
    """Parse command line arguments and return values as dictionary for evaluation."""
    parser = argparse.ArgumentParser(description='A tool to manage student data...')
    subparsers = parser.add_subparsers()
     # general options
    parser.add_argument('-c','--config', dest='config_file', help='config file in local directory')
    parser.add_argument('-drc', dest='dontReplaceClassNames', action='store_true', help='defines whether to replace class names')
    parser.add_argument('-dsdb', dest='dontStoreInDB', action='store_true', help='defines whether to store imported student data in database')
    # create parser for import
    import_parser = subparsers.add_parser('import', description='import student list into bbss', help='')
    import_parser.add_argument('filename_import', type=argparse.FileType('r'), help='file name to import student data from')
    import_choices = ['csv', 'excel']
    import_parser.add_argument('-f', '--format', default=import_choices[0] , help='input student list from a given file format', choices=import_choices)
    #import_parser.set_defaults(func=import_student_data)
    # create parser for export
    export_parser = subparsers.add_parser('export', description='export student list from bbss', help='')
    export_parser.add_argument('filename_export', type=argparse.FileType('w'), help='file name to export student data to')
    export_choices = ['logodidact', 'ad']
    export_parser.add_argument('-f', '--format', default=export_choices[0] , help='file format in which to export student data', choices=export_choices)
    #export_parser.set_defaults(func=export_student_data)
    return parser.parse_args()


if __name__ == '__main__':
    # create logger for this application
    global my_logger
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,maxBytes=262144,backupCount=5)
    logger.addHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    # parse command line options
    global options
    options = parse_command_line()

    # use default config file (config.py) or a given file in directory
    # where this file lies
    try:
        if not options.config_file:
            import config
        else:
            import os.path
            import imp
            comfig_module_name = os.path.splitext(os.path.split(options.config_file)[1])[0]
            f, filename, description = imp.find_module(comfig_module_name)
            config = imp.load_module(comfig_module_name, f, filename, description)
    except ImportError:
        logger.error("Could not load config file.")
        exit()

    # init random number generator for password generation
    random.seed()

    # evaluate given command line options
    if options.format == 'csv':
        # read file into list of students
        read_csv_file(options.filename_import)
        # check for double entries in student list
        check_for_doubles()
        if not options.dontStoreInDB:
            # store newly imported student list in database
            store_students_db()
    if options.format == 'excel':
        logger.error('Import from excel files is not yet supported!')
    if options.format == 'logodidact':
        # write csv file for use in logodidact
        logger.info("Exporting student data for use in logodidact...")
        output_csv_file(options.filename_export)
        logger.info("Exported student data for use in logodidact.")
    if options.format == 'ad':
        setup_ad()
