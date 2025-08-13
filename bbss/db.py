
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
        #sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
        #sqlite3.register_adapter(uuid.UUID, lambda u: memoryview(u.bytes_le))
        # connecting to database
        self.conn = sqlite3.connect(DB_FILENAME) #detect_types=sqlite3.PARSE_DECLTYPES
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
            # TODO: Figure out if it is possible to add foreign key constraint ON DELETE CASCADE to student_id reference?! (Solution: https://www.sqlite.org/faq.html#q11)
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
        if user_version <= 4:
            self.cur.execute("""ALTER TABLE Students ADD COLUMN courses TEXT DEFAULT ""; """)
            self.set_database_version(5)
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
            if callback is not None and callable(callback):
                callback(i, len(student_list))
            current_student = None
            # if imported student has already a GUID...
            if student.guid:
                # ...check if student is already in database by using GUID as identifiers
                sql = 'SELECT * FROM Students WHERE guid=?;'
                self.cur.execute(sql, (str(student.guid), ))
                current_student = self.cur.fetchone()
            # if students GUID is not known...
            if not current_student:
                # ...check if student is already in database by using name and birthday as identifiers
                sql = 'SELECT * FROM Students WHERE surname=? AND firstname=? AND birthday=?;'
                self.cur.execute(sql, (student.surname, student.firstname, student.birthday))
                current_student = self.cur.fetchone()
                # check whether the student with given surname, firstname and
                # birthday has already a GUID (meaning he/she was imported from
                # BBS-Verwaltung, which can store multiple entries for the same
                # student, e.g. students with overlapping membership in multiple
                # classes)
                if current_student and current_student['guid']:
                    logger.debug('Adding second database entry for student: {} {}'.format(
                        current_student['firstname'], current_student['surname']))
                    # allow to include student a second time with the new class assigned to him/her
                    current_student = None
            #
            #
            if not current_student:
                # insert student in database
                logger.debug('Added new student to database: {}'.format(student))
                self.cur.execute('INSERT INTO Students VALUES (NULL,?,?,?,?,?,?,?,?,?)',
                                 (student.surname, student.firstname,
                                  student.classname, student.birthday,
                                  student.generate_user_id(),
                                  student.generate_password(),
                                  student.email, str(student.guid),
                                  student.courses))
                # insert connection between new student and this import
                student_id = self.cur.lastrowid
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?,?)',
                                 (student_id, import_id, student.classname))
            else:
                # get student id from database
                student_id = current_student['id']
                # update email address if option is set
                if config.ALWAYS_IMPORT_EMAIL_ADDRESSES:
                    self.cur.execute('UPDATE Students SET email=? WHERE id=?;',
                                     (student.email, student_id))
                # update GUID for all students, import for previously exiting students!
                self.cur.execute('UPDATE Students SET guid=? WHERE id=?;',
                                 (str(student.guid), student_id))
                # update courses for existing students
                self.cur.execute('UPDATE Students SET courses=? WHERE id=?;',
                                 (str(student.courses), student_id))
                # update firstname, surname and birthday for students identified by GUID
                self.cur.execute('UPDATE Students SET firstname=?, surname=?, birthday=? WHERE id=?;',
                                 (student.firstname, student.surname, student.birthday, student_id))
                # if student changed class between imports, change it
                if current_student['classname'] != student.classname:
                    # update class name
                    self.cur.execute('UPDATE Students SET classname=? WHERE id=?;',
                                     (student.classname, student_id))
                    # store old class name for future reference
                    self.cur.execute('INSERT INTO ClassChanges VALUES (?,?,?);',
                                     (student_id, import_id, current_student['classname']))
                # check whether the student has been in the previous import
                sql = 'SELECT * FROM StudentsInImports WHERE student_id=? AND import_id=?;'
                self.cur.execute(sql, (student_id, import_id-1))
                was_in_previous_import = self.cur.fetchone()
                if config.ALWAYS_OVERWRITE_USERNAME_AND_PASSWORD or not was_in_previous_import:
                    self.cur.execute('UPDATE Students SET username=?, password=? WHERE id=?;',
                                     (student.generate_user_id(regenerate=True),
                                      student.generate_password(regenerate=True),
                                      student_id))
                # ...and include it in current import
                self.cur.execute('INSERT INTO StudentsInImports VALUES (?,?,?)',
                                 (student_id, import_id, student.classname))
        self.conn.commit()

    def print_statistics(self):
        # get statistics
        last_import_id = self.get_last_import_id()
        self.cur.execute("""SELECT import_id, COUNT(*) FROM (
                            SELECT student_id, COUNT(import_id) as cd, import_id
                            FROM StudentsInImports
                            WHERE import_id=? OR import_id=?
                            GROUP BY student_id )
                            WHERE cd = 1 GROUP BY import_id
                            ORDER BY import_id;""",
                         (last_import_id, last_import_id-1))
        result_data = self.cur.fetchall()
        for element in list(result_data):
            if element[0] == last_import_id:
                logger.info('{} students added.'.format(element['count(*)']))
            if element[0] == last_import_id - 1:
                logger.info('{} students removed.'.format(element['count(*)']))
        # get student count
        self.cur.execute('SELECT COUNT(*) FROM Students;')
        result_data = self.cur.fetchone()
        logger.info('{0} students currently stored in database.'
                    .format(result_data['count(*)']))
        self.conn.commit()

    def build_student(self, student, include_dates=False):
        """
        Builds a new Student object from result given by the database.
        """
        ###
        # It is importent to get class from table StudentsInImport instead of table Student,
        # because some students are enrolled in multiple classes and the field classname in
        # table Students does only contain a single class name!
        ###
        s = data.Student(student['surname'], student['firstname'],
                         student['class_in_import'], student['birthday'])
        s.user_id = student['username']
        s.password = student['password']
        s.email = student['email']
        s.guid = student['guid']
        s.courses = student['courses']
        if include_dates:
            s.entry_date, s.exit_date = self._get_entry_and_exit_date_for_student(student['id'])
        return s

    def _get_entry_and_exit_date_for_student(self, student_id):
        """
        Gets entry and exit date for student in the school. It finds the last
        import which contains the student and searches all imports in reverse
        order for the first one. This gives the last consecutive duration were
        the student visited the school.
        """
        latest_import = self.get_last_import_id()
        sql_for_entry_and_exit_date = """
            SELECT Imports.id as import_id, Imports.date as import_date, StudentsInImports.class_in_import
            FROM StudentsInImports
            JOIN Imports ON StudentsInImports.import_id = Imports.id
            WHERE student_id = ? ORDER BY Imports.id DESC;"""
        self.cur.execute(sql_for_entry_and_exit_date, (student_id, ))
        result_data = list(self.cur.fetchall())
        
        #entry_date = None
        #for i, import_data in enumerate(result_data):
        #    current_import = import_data['import_id']
        #    current_date = import_data['import_date']
        #    if i == 0:
        #        # take first date for exit date because descending order by SQL
        #        exit_date = import_data['import_date']
        #    else:
        #        # search for first entry that is not consecutively anymore
        #        if int(import_data['import_id']) < int(current_import)-1:
        #            entry_date = current_date
        #            break
        # just set earliest date if student was consecutively at the school
        #if not entry_date:
        #    entry_date = result_data[-1]['import_date']

        # always set earliest entry as entry date
        entry_date = result_data[-1]['import_date']
        # set exit date if last import for student was not the latest import executed
        if result_data[0]['import_id'] == latest_import:
            exit_date = ''
        else:
            exit_date = result_data[0]['import_date']
        return entry_date, exit_date

    def search_for_student(self, search_string):
        # TODO: Check whether this search gets last class, student is/was in?!
        select_stmt = """SELECT id, surname, firstname, birthday, username, password, email, guid, courses, class_in_import, MAX(import_id)
                         FROM (SELECT * FROM Students
                         WHERE surname LIKE ? OR firstname LIKE ?
                         OR classname LIKE ? OR birthday LIKE ?
                         ) JOIN StudentsInImports ON student_id = id GROUP BY student_id"""
        student_list = []
        search_string = ('%{}%'.format(search_string), ) * 4
        self.cur.execute(select_stmt, search_string)
        result_data = self.cur.fetchall()
        for student in result_data:
            s = self.build_student(student)
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
        sql = 'SELECT id FROM Students WHERE surname=? AND firstname=? AND birthday=?;'
        self.cur.execute(sql, (surname, firstname, birthday))
        current_student = self.cur.fetchone()
        if current_student:
            # get all imports that contain this student
            stmt = 'SELECT import_id FROM StudentsInImports WHERE student_id=?;'
            self.cur.execute(stmt, (current_student['id'], ))
            result_data = self.cur.fetchall()
            return [int(i[0]) for i in result_data]
        else:
            return []

    def generate_changeset(self, old_import_id=-1, new_import_id=0, include_dates=False):
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
            return self._get_all_students_of_import(new_import_id, include_dates=include_dates)
        else:
            return self._get_difference_between_imports(old_import_id, new_import_id,
                                                        include_dates=include_dates)

    def _import_ids_are_wrong(self, old_import_id, new_import_id):
        return (old_import_id >= new_import_id or
                new_import_id > self.get_last_import_id() or
                old_import_id > self.get_last_import_id())

    def _get_difference_between_imports(self, old_import_id, new_import_id, include_dates=False):
        # TODO handle changed students
        sql = """SELECT id, surname, firstname, birthday, username, password, email, guid, courses, classname as class_in_import
                 FROM (
                     SELECT student_id FROM StudentsInImports
                     WHERE import_id=?
                     EXCEPT
                     SELECT student_id FROM StudentsInImports
                     WHERE import_id=?
                 ) JOIN Students ON student_id = id"""
        change_set = data.ChangeSet()

        # get added students and store them in list
        self.cur.execute(sql, (new_import_id, old_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Added students are: ')
        for student in result_data:
            s = self.build_student(student, include_dates=include_dates)
            logger.debug('\t' + str(s))
            # skip student, if already in list, because that can happen, if students are associated with multiple classes
            if s in change_set.students_added:
                logger.warning('Skipping added student that is already in list!')
                continue
            change_set.students_added.append(s)

        # get removed students and store them in list
        self.cur.execute(sql, (old_import_id, new_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Removed students are: ')
        for student in result_data:
            s = self.build_student(student, include_dates=include_dates)
            logger.debug('\t' + str(s))
            change_set.students_removed.append(s)

        # get changed students from database and store them in list
        # TODO: Get changed students without relying on the table ClassChanges!
        changed_student_stmt = """
                               SELECT * FROM (
                                 SELECT Students.id, Students.surname, Students.firstname, Students.classname, Students.birthday,
                                       Students.username, Students.password, Students.email, Students.guid, Students.courses
                                 FROM (
                                    SELECT student_id, import_id FROM ClassChanges WHERE import_id BETWEEN ? AND ?
                                 ) JOIN Students ON student_id = id
                               ) JOIN StudentsInImports ON StudentsInImports.import_id = import_id AND StudentsInImports.student_id = id
                               """ 
        self.cur.execute(changed_student_stmt, (old_import_id + 1, new_import_id))
        result_data = self.cur.fetchall()
        logger.debug('Changed students are: ')
        for student in result_data:
            s = self.build_student(student, include_dates=include_dates)
            logger.debug('\t' + str(s))
            # skip student, if already in list, because that can happen, if students are associated with multiple classes
            if s in change_set.students_changed:
                # delete student entry that is already in list and add new student entry
                # (should pretend wrong class information in exports, because multiple entries
                # are returned from database and only the last one has the correct class info!!!)
                change_set.students_changed.remove(s)
                logger.warning('Skipping changed student that is already in list: {}'.format(s))
            change_set.students_changed.append(s)
        change_set.classes_added, change_set.classes_removed = self._get_class_changes(old_import_id, new_import_id)
        return change_set

    def _get_all_students_of_import(self, new_import_id, include_dates=False):
        """
        Returns all students for a given import.

        :param new_import_id: import ID for which to get students
        :return: ChangeSet object containing all students from the given import
        """
        sql_for_all_students = """SELECT id, import_id,
            student_id, firstname, surname, classname, birthday, username,
            password, email, guid, courses, class_in_import
            FROM StudentsInImports, Students
            WHERE StudentsInImports.student_id = Students.id
            AND import_id = ?; """
        self.cur.execute(sql_for_all_students, (new_import_id, ))
        result_data = self.cur.fetchall()
        # build change set and return it
        change_set = data.ChangeSet()
        for student in result_data:
            s = self.build_student(student, include_dates=include_dates)
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
            AND import_id = ?; """
        # get all classes for old import
        self.cur.execute(classes_for_import_statement, (old_import_id, ))
        result_data = self.cur.fetchall()
        classes_old = [r['class_in_import'] for r in result_data]
        # get all classes for new import
        self.cur.execute(classes_for_import_statement, (new_import_id, ))
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
            AND import_id = ?; """
        # get all classes for new import
        self.cur.execute(classes_for_import_statement, (import_id, ))
        result_data = self.cur.fetchall()
        classes_new = [r['classname'] for r in result_data]
        logger.debug('All classes in import: {}'.format(classes_new))
        return classes_new

    def get_class_history(self, student_id):
        # pylint: disable=unused-variable
        query_id = """SELECT class_in_import as classname, min(import_id) as min_import,
                      max(import_id) as max_import FROM
                      ( SELECT * FROM students JOIN StudentsInImports
	                  ON StudentsInImports.student_id = Students.id ORDER BY Students.id )
                      WHERE username = ? GROUP BY class_in_import ORDER BY import_id;"""
        query_dates = """SELECT classname, I1.date as min_date, I2.date as max_date FROM
                         ( SELECT class_in_import as classname, min(import_id) as min_import,
                         max(import_id) as max_import FROM
                         ( SELECT * FROM students JOIN StudentsInImports
	                     ON StudentsInImports.student_id = Students.id ORDER BY Students.id )
                         WHERE username = ? GROUP BY class_in_import ORDER BY import_id )
                         JOIN Imports as I1 ON min_import = I1.id
                         JOIN Imports as I2 ON (max_import) = I2.id;"""
        self.cur.execute(query_dates, (student_id, ))
        result_data = self.cur.fetchall()
        history = []
        for r in result_data:
            history.append((r['classname'], r['min_date'], r['max_date']))
        return history


    def delete_old_data(self, retention_period, callback):
        """
        Removes all students that have not been in an import for a given
		retention period. All entries in the tables Students and
		StudentsInImports will be deleted. The entries in the Imports table
		will NOT be deleted!

        :param retention_period: period for which not to delete student data
		:param callback: Function that is called after each deletion of a
                         student. First parameter is the number of the current
                         deleted student, second parameter is the number of
                         students to be deleted.
        :return: list of all deleted students
        """
        student_query = """SELECT student_id, max(import_id) as max_import
                           FROM StudentsInImports JOIN Students
                           ON StudentsInImports.student_id = Students.id
                           GROUP BY student_id HAVING max(import_id) < ?
                           ORDER BY student_id;"""
        # find first import to be kept in the database
        self.cur.execute('SELECT min(id), date FROM imports WHERE date > ?;', (retention_period, ))
        result_data = self.cur.fetchall()
        minimal_import = result_data[0]['min(id)']
        # TODO: Check whether minimal import is last import?!
        logger.info('First import that should be kept in the database: {}'.format(minimal_import))
        # find the last import for all students and filter them
        self.cur.execute(student_query, (minimal_import, ))
        result_data = self.cur.fetchall()
        with self.conn:
            # delete all students that appear only in older imports
            for i, r in enumerate(result_data):
                # call callback functions with number of current students
                if callback is not None and callable(callback):
                    callback(i, len(result_data))
                student_id = r['student_id']
                logger.debug('Deleting student no. {} with last import no. {}.'.format(*tuple(r)))
                self.conn.execute("DELETE FROM StudentsInImports WHERE student_id=?;", (student_id, ))
                self.conn.execute("DELETE FROM Students WHERE id=?;", (student_id, ))
            else:
                logger.info('Deleted {} students from database.'.format(i))
        # compressing database file
        logger.info('Compressing database file...')
        with self.conn:
            self.conn.execute('VACUUM;')

    def get_usernames_and_ids(self):
        cs = self.generate_changeset(old_import_id=0, new_import_id=0)
        return [(s.guid, s.user_id) for s in cs.students_added]

    def close_connection(self):
        """Closes connection to database."""
        self.conn.close()
