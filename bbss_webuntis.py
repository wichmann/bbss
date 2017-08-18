#! /usr/bin/env python3

"""
bbss - BBS Student Management

Quick fix to recreate a PDF file from already stored CSV file.

Created on Thu Aug  17 17:37:42 2017

@author: Christian Wichmann
"""

import sys
import csv
import logging
import logging.handlers

from bbss import webuntis


def main():
    list_of_passwords = {}
    if len(sys.argv) != 3:
        logger.error('Data file missing. Usage: ./bbss_webuntis.py data.txt output.pdf')
        return
    data_file = sys.argv[1]
    output_file = sys.argv[2]
    # read old data file
    with open(data_file, 'r', newline='', encoding='utf8') as csvfile:
        data_file_reader = csv.reader(csvfile)
        # skip file header
        next(data_file_reader)
        for row in data_file_reader:
            list_of_passwords[row[0]] = row[2]
    webuntis.create_pdf_doc(output_file, list_of_passwords)


if __name__ == '__main__':
    # create logger for this application
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss')
    logger.setLevel(logging.DEBUG)
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=262144, backupCount=5)
    log_to_file.setLevel(logging.DEBUG)
    logger.addHandler(log_to_file)
    log_to_screen = logging.StreamHandler(sys.stdout)
    log_to_screen.setLevel(logging.INFO)
    logger.addHandler(log_to_screen)
    main()
