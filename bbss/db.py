
"""
bbss - BBS Student Management

StudentDatabase class is used as DAO for accessing the students database and
calculating changes when importing a new set of student data.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import sqlite3
import datetime
import logging

from bbss import data

logger = logging.getLogger('bbss.db')

DB_FILENAME = 'students.db'


class StudentDatabase(object):
    """Connects to database and allows to store and get student data."""
    def __init__(self):
        """Initializes a new database to store student information."""
        logger.info('Initializing student database...')
        # connecting to database
        self.conn = sqlite3.connect(DB_FILENAME)
        # change the row factory to use Row to allow access via column name
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.close_connection()

    def create_tables(self):
        """Creates tables for database, if they not already exist."""
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Imports (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT NOT NULL, date DATE NOT NULL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Students (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            surname TEXT NOT NULL, firstname TEXT NOT NULL,
                            classname TEXT NOT NULL, birthday DATE NOT NULL,
                            username TEXT NOT NULL, password TEXT NOT NULL)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS StudentsInImports (
                            student_id INT NOT NULL, import_id INT NOT NULL,
                            FOREIGN KEY(student_id) REFERENCES Students(id),
                            FOREIGN KEY(import_id) REFERENCES Imports(id))""")
        self.conn.commit()

    def get_last_import_id(self):
        """Gets index of last import from database."""
        self.cur.execute('SELECT MAX(id) FROM Imports')
        result_data = self.cur.fetchone()
        return result_data['max(id)']

    def store_students_db(self, importfile_name, student_list):
        """Stores a new complete set of students in the database. Already
           imported students will only be referenced and their user name and
           password information will not be altered."""

        # storing new data in database
        self.cur.execute("INSERT INTO Imports VALUES(NULL,?,?)",
                         (importfile_name, datetime.date.today()))
        import_id = self.cur.lastrowid
        self.conn.commit()

        # storing all students in database
        for student in student_list:
            # check if student is already in database
            sql = """SELECT * FROM Students
                     WHERE surname="{0}" AND firstname="{1}"
                     AND birthday="{2}" """.format(student.surname,
                                                   student.firstname,
                                                   student.birthday)
            self.cur.execute(sql)
            if not self.cur.fetchone():
                # insert student in database
                self.cur.execute("""INSERT INTO Students
                                    VALUES (NULL,?,?,?,?,?,?)""",
                                 (student.surname, student.firstname,
                                  student.classname, student.birthday,
                                  student.generate_user_id(),
                                  student.generate_password()))
                # insert connection between new student and this import
                student_id = self.cur.lastrowid
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?)',
                                 (student_id, import_id))
            else:
                # change already stored student
                self.cur.execute("""UPDATE Students SET classname=?,
                                    username=?, password=?
                                    WHERE surname=? AND firstname=?
                                    AND birthday=? """,
                                 (student.classname,
                                  student.generate_user_id(),
                                  student.generate_password(),
                                  student.surname,
                                  student.firstname,
                                  student.birthday))
                self.cur.execute("""SELECT * FROM Students WHERE surname=?
                                    AND firstname=? AND birthday=?""",
                                 (student.surname,
                                  student.firstname,
                                  student.birthday))
                result_data = self.cur.fetchone()
                student_id = result_data[0]
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?)',
                                 (student_id, import_id))
        self.conn.commit()

    def print_statistics(self):
        # get statistics
        last_import_id = self.get_last_import_id()
        self.cur.execute("""SELECT import_id, COUNT(*) FROM (
                            SELECT student_id,
                            COUNT(import_id) as cd, import_id
                            FROM StudentsInImports
                            WHERE import_id = {0} OR import_id = {1}
                            GROUP BY student_id )
                            WHERE cd = 1 GROUP BY import_id
                            ORDER BY import_id;"""
                         .format(last_import_id, last_import_id - 1))
        result_data = self.cur.fetchall()
        for element in list(result_data):
            if element[0] == last_import_id:
                logger.info('%s students added.' % element['count(*)'])
            if element[0] == last_import_id - 1:
                logger.info('%s students removed.' % element['count(*)'])
        # get student count
        self.cur.execute('SELECT COUNT(*) FROM Students')
        result_data = self.cur.fetchone()
        logger.info('{0} students currently stored in database.'
                    .format(result_data['count(*)']))
        self.conn.commit()

    def search_for_student(self, search_string):
        select_stmt = """SELECT * FROM Students
                         WHERE surname LIKE "%{0}%"
                         OR firstname LIKE "%{0}%"
                         OR classname LIKE "%{0}%"
                         OR birthday LIKE "%{0}%" """
        student_list = []
        self.cur.execute(select_stmt.format(search_string))
        result_data = self.cur.fetchall()
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            student_list.append(s)
        return student_list

    def generate_changeset(self, old_import_id=0, new_import_id=0):
        """Generates a changeset with all added, deleted and changed student
           data between two specific imports.

           As parameters two imports can be selected by their IDs. Both
           parameters must be positive integer values.

           If no old import ID is given the last import before the new import
           ID is used. When no new import ID is given, the change set will
           contain all changes between the old import and the latest one. If
           neither an old nor a new import ID was set the change set will be
           generated by comparing the next to last and the latest import.

           Example:

           Database contains 6 imports of student data.

           generate_changeset() -> changes between import 5 and 6
           generate_changeset(new_import_id=5)
                                -> changes between import 4 and 5
           generate_changeset(old_import_id=2)
                                -> changes between import 2 and 6
           generate_changeset(old_import_id=3, new_import_id=5)
                                -> changes between import 3 and 5
           """
        if old_import_id < 0 or new_import_id < 0:
            raise ValueError
        # fill in not given IDs
        if new_import_id == 0:
            # get lastest import ID from database if no ID was given
            new_import_id = self.get_last_import_id()
            logger.debug('New import ID set to {0}.'.format(new_import_id))
        if old_import_id == 0:
            # set old import ID to new import ID minus one if no ID was given
            old_import_id = new_import_id - 1
            logger.debug('Old import ID set to {0}.'.format(old_import_id))
        # check for implausible import IDs
        if self._import_ids_are_wrong(old_import_id, new_import_id):
            return data.ChangeSet()
        # get student data from database
        logger.info('Getting student data between imports no. {0} and no. {1}'
                    .format(old_import_id, new_import_id))
        if old_import_id == 1:
            return self._get_all_students_of_import(new_import_id)
        else:
            return self._get_difference_between_imports(old_import_id,
                                                        new_import_id)

    def _import_ids_are_wrong(self, old_import_id, new_import_id):
        return (old_import_id >= new_import_id or
                new_import_id > self.get_last_import_id() or
                old_import_id > self.get_last_import_id())

    def _get_difference_between_imports(self, old_import_id, new_import_id):
        # TODO handle changed students
        sql = """SELECT * FROM
                 (
                 SELECT student_id FROM StudentsInImports
                 WHERE import_id = {0}
                 EXCEPT
                 SELECT student_id FROM StudentsInImports
                 WHERE import_id = {1}
                 )
                 JOIN Students ON student_id = id"""
        change_set = data.ChangeSet()

        # get added students and store them in list
        self.cur.execute(sql.format(old_import_id, new_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Added students are: ')
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            logger.debug('\t' + str(s))
            change_set.students_added.append(s)

        # get removed students and store them in list
        self.cur.execute(sql.format(new_import_id, old_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Removed students are: ')
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            logger.debug('\t' + str(s))
            change_set.students_removed.append(s)

        return change_set

    def _get_all_students_of_import(self, new_import_id):
        sql_for_all_students = """SELECT import_id,
            student_id, firstname, surname,
            classname, birthday
            FROM StudentsInImports, Students
            WHERE StudentsInImports.student_id = Students.id
            AND import_id = "{0}"; """.format(new_import_id)
        self.cur.execute(sql_for_all_students)
        result_data = self.cur.fetchall()
        # build change set and return it
        change_set = data.ChangeSet()
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            change_set.students_added.append(s)
        return change_set

    def close_connection(self):
        """Closes connection to database."""
        self.conn.close()
