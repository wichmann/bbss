
"""
bbss - BBS Student Management

Reads student data from csv files and stores them in a database. Data can be
exported to be used by other systems like AD or RADIUS servers.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""


import csv
import sqlite3
import datetime
import logging

from bbss import config
from bbss import data


logger = logging.getLogger('bbss.main')


student_list = []

### correlation between columns in the csv file and their attributes
column_map = {'surname': 0,
              'firstname': 0,
              'classname': 0,
              'birthday': 0}


def read_csv_file(input_file, replace_classnames):
    """reads a csv file and adds student to list"""
    logger.info('Importing student from file...')

    global do_replace_classnames
    do_replace_classnames = replace_classnames

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


def output_csv_file(output_file):
    """outputs a csv file with all information for all students for the AD"""
    logger.info('Writing student data to csv file...')
    output_file_writer = csv.writer(output_file, delimiter=';')
    output_file_writer.writerow(('Class', 'Name', 'Firstname', 'UserID',
                                 'Password', 'OU'))
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


def store_students_db(importfile_name):
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
    cur.execute("INSERT INTO Imports VALUES(NULL,?,?)", (importfile_name, datetime.date.today()))
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
            cur.execute('SELECT * FROM Students WHERE surname=? AND firstname=? AND birthday=?', (student.surname, student.firstname, student.birthday))
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
