
"""
bbss - BBS Student Management

StudentDatabase class is used as DAO for accessing the students database and
calculating changes when importing a new set of student data.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import uuid
import sqlite3
import datetime
import logging

from bbss import data
from bbss import config

logger = logging.getLogger('bbss.db')

DB_FILENAME = 'students.db'


#
# Technical notes on database schema:
#
# In the first version of this program, the database stored the class
# information for all students in the table "Students". Problems occurred
# when students changed classes or visited multiple school types after another.
#
# Since September 2015 at each import the class of a student is stored with
# the student data in table "Student" and also in the field "class_in_import"
# in the "StudentsInImports" table.
#
# While old entries are still in the database, information about which student
# changed class between imports has to be stored. Therefore an additional table
# ("ClassChanges") is created, that contains a student id of the student
# changing class, the import id of the import in which the class changes took
# place and the old class name before the import.
#


class StudentDatabase(object):
    """Connects to database and allows to store and get student data."""
    def __init__(self):
        """Initializes a new database to store student information."""
        logger.info('Initializing student database...')
        # register adapters for storing and getting UUID to/from database
        # source: https://stackoverflow.com/a/18842491
        sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
        sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))
        # connecting to database
        self.conn = sqlite3.connect(DB_FILENAME)
        # change the row factory to use Row to allow access via column name
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.close_connection()

    def create_tables(self):
        """
        Creates or alter tables for student database, if they not already exist.
        To know which tables have to be updated or created, an user version is
        stored as PRAGMA inside the database.

        Per default the version is "0" if a new database is created. In the first
        version the tables Imports, Students and StudentsInImports are created.
        The second version (September 2015) changed how the class information is
        stored. (See technical note above!)
        """
        user_version = self.get_database_version()
        if user_version == 0:
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
            self.set_database_version(1)
        if user_version <= 1:
            self.cur.execute("""ALTER TABLE StudentsInImports ADD COLUMN class_in_import TEXT DEFAULT ""; """)
            self.cur.execute("""CREATE TABLE IF NOT EXISTS ClassChanges (
                                student_id INT NOT NULL, import_id INT NOT NULL,
                                old_class_name TEXT NOT NULL,
                                FOREIGN KEY(student_id) REFERENCES Students(id),
                                FOREIGN KEY(import_id) REFERENCES Imports(id))""")
            self.set_database_version(2)
        if user_version <= 2:
            self.cur.execute("""ALTER TABLE Students ADD COLUMN email TEXT DEFAULT ""; """)
            self.set_database_version(3)
        if user_version <= 3:
            self.cur.execute("""ALTER TABLE Students ADD COLUMN guid GUID DEFAULT ""; """)
            self.set_database_version(4)
        self.conn.commit()

    def set_database_version(self, new_version):
        self.cur.execute('PRAGMA user_version={};'.format(new_version))
        self.conn.commit()
        logger.debug('Updating database version to: {}'.format(new_version))

    def get_database_version(self):
        self.cur.execute('PRAGMA user_version;')
        user_version = self.cur.fetchone()[0]
        logger.debug('Current database version: {}'.format(user_version))
        return user_version

    def get_last_import_id(self):
        """Gets index of last import from database."""
        self.cur.execute('SELECT MAX(id) FROM Imports')
        result_data = self.cur.fetchone()
        last_import_id = result_data['max(id)']
        if last_import_id:
            return last_import_id
        else:
            return 0

    def store_students_db(self, importfile_name, student_list, callback):
        """
        Stores a new complete set of students in the database. Already imported
        students will only be referenced and their user name and password
        information will not be altered.
        
        :param importfile_name: name of the file from which the students were
                                imported
        :param student_list: list with the student data that should be imported
                             into the database
        :param callback: Function that is called after each of the students
                         that are imported. First parameter is the current
                         imported student, second parameter is the number of
                         students to be imported.
        """
        # store import date and filename in database
        self.cur.execute("INSERT INTO Imports VALUES(NULL,?,?)",
                         (importfile_name, datetime.date.today()))
        import_id = self.cur.lastrowid
        self.conn.commit()

        # storing all students in database
        for i, student in enumerate(student_list):
            # call callback functions with number of current students
            if callback != None and callable(callback):
                callback(i, len(student_list))
            current_student = None
            # if imported student has already a GUID...
            if student.guid:
                # ...check if student is already in database by using GUID as identifiers
                sql = """SELECT * FROM Students WHERE guid=?; """
                self.cur.execute(sql, (str(student.guid), ))
                current_student = self.cur.fetchone()
            # if students GUID is not known...
            if not current_student:
                # ...check if student is already in database by using name and birthday as identifiers
                sql = """SELECT * FROM Students
                         WHERE surname="{0}" AND firstname="{1}" AND birthday="{2}";
                      """.format(student.surname, student.firstname, student.birthday)
                self.cur.execute(sql)
                current_student = self.cur.fetchone()
            if not current_student:
                # insert student in database
                self.cur.execute("""INSERT INTO Students VALUES (NULL,?,?,?,?,?,?,?,?)""",
                                 (student.surname, student.firstname,
                                  student.classname, student.birthday,
                                  student.generate_user_id(),
                                  student.generate_password(),
                                  student.email, str(student.guid)))
                # insert connection between new student and this import
                student_id = self.cur.lastrowid
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?,?)',
                                 (student_id, import_id, student.classname))
            else:
                # get student id from database
                student_id = current_student['id']
                # update email address if option is set
                if config.ALWAYS_IMPORT_EMAIL_ADDRESSES:
                    self.cur.execute("""UPDATE Students SET email=?
                                        WHERE surname=? AND firstname=? AND birthday=?;""",
                                     (student.email, student.surname, student.firstname, student.birthday))
                # if student changed class between imports, change it
                if current_student['classname'] != student.classname:
                    # update class name
                    self.cur.execute("""UPDATE Students SET classname=?
                                        WHERE surname=? AND firstname=? AND birthday=?;""",
                                     (student.classname, student.surname,
                                      student.firstname, student.birthday))
                    # store old class name for future reference
                    self.cur.execute("""INSERT INTO ClassChanges VALUES (?,?,?);""",
                                     (student_id, import_id, current_student['classname']))
                # check whether the student has been in the previous import
                sql = 'SELECT * FROM StudentsInImports WHERE student_id = {} AND import_id = {};'
                self.cur.execute(sql.format(student_id, import_id - 1))
                was_in_previous_import = self.cur.fetchone()
                if config.ALWAYS_OVERWRITE_USERNAME_AND_PASSWORD or not was_in_previous_import:
                    self.cur.execute("""UPDATE Students SET username=?, password=?
                                        WHERE surname=? AND firstname=? AND birthday=? """,
                                     (student.generate_user_id(regenerate=True),
                                      student.generate_password(regenerate=True),
                                      student.surname, student.firstname, student.birthday))
                # ...and include it in current import
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?,?)',
                                 (student_id, import_id, student.classname))
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
            # get data for each and every found student into one list of
            # Student objects
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            s.user_id = student['username']
            s.password = student['password']
            s.email = student['email']
            student_list.append(s)
        return student_list

    def get_imports_for_student(self, firstname, surname, birthday):
        """
        Returns a list with the import IDs for all imports that contain the
        given student identified by her surname, firstname and birthday.

        :param firstname: firstname of student to be found
        :param surname: surname of student to be found
        :param birthday: birthday of student to be found
        :return: list with all imports that contain the given student
        """
        # get student ID from database
        sql = """SELECT id FROM Students WHERE surname="{0}" AND firstname="{1}" AND birthday="{2}";
              """.format(surname, firstname, birthday)
        self.cur.execute(sql)
        current_student = self.cur.fetchone()
        if current_student:
            # get all imports that contain this student
            get_all_imports_stmt = """SELECT import_id FROM StudentsInImports
                                      WHERE student_id = {};"""
            self.cur.execute(get_all_imports_stmt.format(current_student['id']))
            result_data = self.cur.fetchall()
            return [int(i[0]) for i in result_data]
        else:
            return []

    def generate_changeset(self, old_import_id=-1, new_import_id=0):
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
        if old_import_id < -1 or new_import_id < 0:
            #raise ValueError
            logger.error('Given import ids are not valid!')
            return data.ChangeSet()
        # fill in not given IDs
        if new_import_id == 0:
            # get lastest import ID from database if no ID was given
            new_import_id = self.get_last_import_id()
            logger.debug('New import ID set to {0}.'.format(new_import_id))
        if old_import_id == -1:
            # set old import ID to new import ID minus one if no ID was given
            old_import_id = new_import_id - 1
            logger.debug('Old import ID set to {0}.'.format(old_import_id))
        # check for implausible import IDs
        if self._import_ids_are_wrong(old_import_id, new_import_id):
            return data.ChangeSet()
        # get student data from database
        logger.debug('Getting student data between imports no. {0} and no. {1}'
                     .format(old_import_id, new_import_id))
        if old_import_id == 0:
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
        sql = """SELECT * FROM (
                     SELECT student_id FROM StudentsInImports
                     WHERE import_id = {0}
                     EXCEPT
                     SELECT student_id FROM StudentsInImports
                     WHERE import_id = {1}
                 ) JOIN Students ON student_id = id"""
        change_set = data.ChangeSet()

        # get added students and store them in list
        self.cur.execute(sql.format(new_import_id, old_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Added students are: ')
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            s.user_id = student['username']
            s.password = student['password']
            s.email = student['email']
            logger.debug('\t' + str(s))
            change_set.students_added.append(s)

        # get removed students and store them in list
        self.cur.execute(sql.format(old_import_id, new_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Removed students are: ')
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            s.user_id = student['username']
            s.password = student['password']
            s.email = student['email']
            logger.debug('\t' + str(s))
            change_set.students_removed.append(s)

        # get changed students from database and store them in list
        changed_student_stmt = """SELECT * FROM (
                                  SELECT student_id FROM ClassChanges
                                  WHERE import_id BETWEEN {0} AND {1}
                                  ) JOIN Students ON student_id = id"""
        self.cur.execute(changed_student_stmt.format(old_import_id + 1, new_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Changed students are: ')
        for student in result_data:
            s = data.Student(student['surname'],
                             student['firstname'],
                             student['classname'],
                             student['birthday'])
            s.user_id = student['username']
            s.password = student['password']
            s.email = student['email']
            logger.debug('\t' + str(s))
            change_set.students_changed.append(s)
        change_set.classes_added, change_set.classes_removed = self._get_class_changes(old_import_id, new_import_id)
        return change_set

    def _get_all_students_of_import(self, new_import_id):
        """
        Returns all students for a given import.
        
        :param new_import_id: import ID for which to get students
        :return: ChangeSet object containing all students from the given import
        """
        sql_for_all_students = """SELECT import_id,
            student_id, firstname, surname,
            classname, birthday, username, password, email
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
            s.user_id = student['username']
            s.password = student['password']
            s.email = student['email']
            change_set.students_added.append(s)
        change_set.classes_added = self._get_all_classes(new_import_id)
        return change_set

    def _get_class_changes(self, old_import_id, new_import_id):
        """
        Compares two imports and returns lists of added/removed classes between
        the given imports.
        
        :param old_import_id: import ID for earlier import of comparison
        :param new_import_id: import ID for later import of comparison
        :return: two lists with the classes that were added and removed between given imports
        """
        classes_added = []
        classes_removed = []
        classes_for_import_statement = """SELECT DISTINCT class_in_import
            FROM StudentsInImports, Students
            WHERE StudentsInImports.student_id = Students.id
            AND import_id = {import_id}; """
        # get all classes for old import
        self.cur.execute(classes_for_import_statement.format(import_id=old_import_id))
        result_data = self.cur.fetchall()
        classes_old = [r['class_in_import'] for r in result_data]
        # get all classes for new import
        self.cur.execute(classes_for_import_statement.format(import_id=new_import_id))
        result_data = self.cur.fetchall()
        classes_new = [r['class_in_import'] for r in result_data]
        # check what classes were added or removed between imports
        classes_removed = list(set(classes_old) - set(classes_new))
        classes_added = list(set(classes_new) - set(classes_old))
        logger.debug('Removed classes: {}'.format(classes_removed))
        logger.debug('Added classes: {}'.format(classes_added))
        return classes_added, classes_removed

    def _get_all_classes(self, import_id):
        classes_for_import_statement = """SELECT DISTINCT classname
            FROM StudentsInImports, Students
            WHERE StudentsInImports.student_id = Students.id
            AND import_id = "{0}"; """
        # get all classes for new import
        self.cur.execute(classes_for_import_statement.format(import_id))
        result_data = self.cur.fetchall()
        classes_new = [r['classname'] for r in result_data]
        logger.debug('All classes in import: {}'.format(classes_new))
        return classes_new

    def close_connection(self):
        """Closes connection to database."""
        self.conn.close()
