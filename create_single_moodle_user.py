#! /usr/bin/env python3

"""
Builds a file to be imported into Moodle to create a single user and make a user
card to distribute the user name and password.

Python dependencies:
 - reportlab

@author: Christian Wichmann
"""

import sys
import datetime
import logging
import logging.handlers

from bbss import pdf
from bbss import data
from bbss import moodle


if __name__ == '__main__':
    # create logger for this application
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss')
    logger.setLevel(logging.DEBUG)
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=262144, backupCount=5, encoding='utf-8')
    log_to_file.setLevel(logging.DEBUG)
    logger.addHandler(log_to_file)
    log_to_screen = logging.StreamHandler(sys.stdout)
    log_to_screen.setLevel(logging.INFO)
    logger.addHandler(log_to_screen)

    student_list = []

    s1 = data.Student('surname', 'firstname', 'classname', '01.01.1980')
    s1.user_id = 'username'
    s1.password = 'passwort'
    s1.email = 'user@domain.com'
    student_list.append(s1)

    s2 = data.Student('surname', 'firstname', 'classname', '01.01.1980')
    s2.user_id = 'username'
    s2.password = 'passwort'
    s2.email = 'user@domain.com'
    student_list.append(s2)

    s3 = data.Student('surname', 'firstname', 'classname', '01.01.1980')
    s3.user_id = 'username'
    s3.password = 'passwort'
    s3.email = 'user@domain.com'
    student_list.append(s3)

    changeset = data.ChangeSet()
    changeset.students_added.extend(student_list)

    # write file for Moodle import and PDF with account data
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    moodle._write_student_list_file('Sonderimport_Moodle_{}.csv'.format(now), changeset, False)
    pdf.export_data('Sonderimport_Moodle_{}.pdf'.format(now), student_list)
