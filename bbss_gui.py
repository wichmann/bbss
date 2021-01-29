#! /usr/bin/env python3

"""
bbss - BBS Student Management

GUI interface for bbss.

Python dependencies:
 - win32com (for Active Directory export)
 -

Created on Mon Feb  26 21:07:36 2014

@author: Christian Wichmann
"""

import logging
import logging.handlers
import sys

from gui import gui


if __name__ == '__main__':
    # create logger for this application
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss')
    logger.setLevel(logging.DEBUG)
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=262144,
                                                       backupCount=5, encoding='utf-8')
    log_to_file.setLevel(logging.DEBUG)
    logger.addHandler(log_to_file)
    log_to_screen = logging.StreamHandler(sys.stdout)
    log_to_screen.setLevel(logging.INFO)
    logger.addHandler(log_to_screen)

    logger.info('Starting gui...')
    gui.start_gui()
