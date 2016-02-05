
"""
bbss - BBS Student Management

Imports and exports student data from Microsoft Excel xls files.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""


import logging
import datetime
import xlrd

from bbss import data


__all__ = ['import_data']


logger = logging.getLogger('bbss.xls')


### correlation between columns in the csv file and their attributes
column_map = {'surname': 0,
              'firstname': 0,
              'classname': 0,
              'birthday': 0}


def import_data(import_file, callback):
    student_count = 0
    student_list = []
    # open excel file
    book = xlrd.open_workbook(import_file)
    sheet = book.sheet_by_index(0)
    # find columns from file
    for i in range(sheet.ncols):
        table_heading_cell = sheet.cell(0, i).value
        if table_heading_cell == 'KL_NAME':
            column_map['classname'] = i
        elif table_heading_cell == 'NNAME':
            column_map['surname'] = i
        elif table_heading_cell == 'VNAME':
            column_map['firstname'] = i
        elif table_heading_cell == 'GEBDAT':
            column_map['birthday'] = i
    # read all rows of table and save them as student objects
    for i in range(1, sheet.nrows):
        # call callback functions with number of current students
        if callback != None and callable(callback):
            callback(i, sheet.nrows)
        # TODO add check with cell.ctype == XL_CELL_TEXT
        class_of_student = sheet.cell(i, column_map['classname']).value
        name_of_student = sheet.cell(i, column_map['surname']).value
        firstname_of_student = sheet.cell(i, column_map['firstname']).value
        # read and convert date from excel format
        try:
            excel_date = xlrd.xldate_as_tuple(sheet.cell(i, column_map['birthday']).value, book.datemode)
            birthday_of_student = datetime.datetime(*excel_date).date()
        except TypeError:
            # if a student has no birthday in BBS Planung the cell is empty and
            # contains a string instead of a datetime, so a TypeError is raised
            birthday_of_student = datetime.datetime(1980, 1, 1)
        # check if student or class is blacklisted
        if data.is_class_blacklisted(class_of_student):
            logger.debug('Student ({0} {1}) not imported because class ({2}) is blacklisted.'
                         .format(firstname_of_student,
                                 name_of_student,
                                 class_of_student))
            continue
        if class_of_student[:2] == 'ZZ':
            logger.debug('Student ({0} {1}) not imported because class ({2}) is blacklisted.'
                         .format(firstname_of_student,
                                 name_of_student,
                                 class_of_student))
            continue
        # check if students name ends with a underscore, because this is an
        # entry for a student that participates in two classes at the same time
        if name_of_student[-1:] == '_':
            continue
        # add student to list
        student_list.append(data.Student(name_of_student,
                                         firstname_of_student,
                                         class_of_student,
                                         birthday_of_student))
        student_count += 1
    logger.info('%s student imported.' % student_count)
    return student_list
