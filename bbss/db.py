
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


logger = logging.getLogger('bbss.data')

DB_FILENAME = 'students.db'


class StudentDatabase(object):
    def __init__(self):
        """Initializes a new database to store student information."""
        logger.info('Storing student data into database...')
        # connecting to database
        self.conn = sqlite3.connect(DB_FILENAME)
        # change the row factory to use Row to allow access via column name
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Creates tables for database, if they not already exist."""
        self.cur.execute("CREATE TABLE IF NOT EXISTS Imports(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL, date DATE NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS Students(id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT NOT NULL, firstname TEXT NOT NULL, classname TEXT NOT NULL, birthday DATE NOT NULL)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS StudentsInImports(student_id INT NOT NULL, import_id INT NOT NULL, FOREIGN KEY(student_id) REFERENCES Students(id), FOREIGN KEY(import_id) REFERENCES Imports(id))")
        self.conn.commit()

    def get_last_import_id(self):
        """Gets index of last import from database."""
        self.cur.execute('SELECT MAX(id) FROM Imports')
        result_data = self.cur.fetchone()
        return result_data['max(id)']
        
    def store_students_db(self, importfile_name, student_list):
        """Stores a new complete set of students in the databse. Already
           imported students will only be referenced and their user name and
           password information will not be altered."""

        # storing new data in database
        self.cur.execute("INSERT INTO Imports VALUES(NULL,?,?)", (importfile_name, datetime.date.today()))
        import_id = self.cur.lastrowid
        self.conn.commit()

        # storing all students in database
        for student in student_list:
            # check if student is already in database
            self.cur.execute('SELECT * FROM Students WHERE surname=? AND firstname=? AND birthday=?', (student.surname, student.firstname, student.birthday))
            if not self.cur.fetchone():
                # insert student in database
                self.cur.execute('INSERT INTO Students VALUES (NULL,?,?,?,?)', (student.surname, student.firstname, student.classname, student.birthday))
                # insert connection between new student and this import
                student_id = self.cur.lastrowid
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?)', (student_id, import_id))
            else:
                # change already stored student
                self.cur.execute('UPDATE Students SET classname=? WHERE surname=? AND firstname=? AND birthday=?', (student.classname, student.surname, student.firstname, student.birthday))
                self.cur.execute('SELECT * FROM Students WHERE surname=? AND firstname=? AND birthday=?', (student.surname, student.firstname, student.birthday))
                result_data = self.cur.fetchone()
                student_id = result_data[0]
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?)', (student_id, import_id))
        self.conn.commit()

    def print_statistics(self):
        # get statistics
        last_import_id = self.get_last_import_id()
        self.cur.execute("""SELECT import_id, COUNT(*)
                       FROM (
                    SELECT student_id, COUNT(import_id) as cd, import_id
                 FROM StudentsInImports
                 WHERE import_id = %s OR import_id = %s
                 GROUP BY student_id
               )
               WHERE cd = 1
               GROUP BY import_id
               ORDER BY import_id;""" % (last_import_id, last_import_id - 1))
        result_data = self.cur.fetchall()
        for element in list(result_data):
            if element[0] == last_import_id:
                logger.info('%s students added.' % element['count(*)'])
            if element[0] == last_import_id - 1:
                logger.info('%s students removed.' % element['count(*)'])

        # get student count
        self.cur.execute('SELECT COUNT(*) FROM Students')
        result_data = self.cur.fetchone()
        logger.info('%s students currently stored in database.' % result_data['count(*)'])
        self.conn.commit()

    def generate_last_changeset(self):
        last_import_id = self.get_last_import_id()
        # get added students
        self.cur.execute("""SELECT import_id, COUNT(*)
                       FROM (
                    SELECT student_id, COUNT(import_id) as cd, import_id
                 FROM StudentsInImports
                 WHERE import_id = %s OR import_id = %s
                 GROUP BY student_id
               )
               WHERE cd = 1
               GROUP BY import_id
               ORDER BY import_id;""" % (last_import_id, last_import_id - 1))
        result_data = self.cur.fetchall()

    def close_connection(self):
        """Closes connection to database."""
        self.conn.close()

    def __del__(self):
        self.close_connection()
