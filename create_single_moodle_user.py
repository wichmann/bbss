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

    # create all necessary data structures and fill in the account data
    s = data.Student('surname', 'firstname', 'classname', '01.01.1980')
    s.user_id = 'username'
    s.password = 'passwort'
    s.email = 'user@domain.com'
    student_list = [s]
    changeset = data.ChangeSet()
    changeset.students_added.append(s)

    # write file for Moodle import and PDF with account data
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    moodle._write_student_list_file('Sonderimport_Moodle_{}.csv'.format(now), changeset, False)
    pdf.export_data('Sonderimport_Moodle_{}.pdf'.format(now), student_list)
