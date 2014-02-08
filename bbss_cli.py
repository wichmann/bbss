#! /usr/bin/env python3

"""
bbss - BBS Student Management

Command line interface for bbss.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import argparse
import logging
import logging.handlers
import sys

from bbss import bbss


def parse_command_line():
    """Parse command line arguments and return values as dictionary for evaluation."""
    parser = argparse.ArgumentParser(description='A tool to manage student data...')
    subparsers = parser.add_subparsers()
     # general options
    parser.add_argument('-c', '--config', dest='config_file',
                        help='config file in local directory')
    parser.add_argument('-drc', dest='dontReplaceClassNames',
                        action='store_true',
                        help='defines whether to replace class names')
    parser.add_argument('-dsdb', dest='dontStoreInDB', action='store_true',
                        help='defines whether to store imported student data in database')
    # create parser for import
    import_parser = subparsers.add_parser('import', 
                                          description='import student list into bbss',
                                          help='')
    import_parser.add_argument('filename_import', help='file name to import student data from')
    import_choices = ['csv', 'excel']
    import_parser.add_argument('-f', '--format', dest="format_choice", default=import_choices[0], help='input student list from a given file format', choices=import_choices)
    #import_parser.set_defaults(func=import_student_data)
    # create parser for export
    export_parser = subparsers.add_parser('export', description='export student list from bbss', help='')
    export_parser.add_argument('filename_export',
                               help='file name to export student data to')
    export_choices = ['logodidact', 'ad']
    export_parser.add_argument('-f', '--format', dest="format_choice", default=export_choices[0], help='file format in which to export student data', choices=export_choices)
    #export_parser.set_defaults(func=export_student_data)
    return parser.parse_args()


if __name__ == '__main__':
    # create logger for this application
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                   maxBytes=262144,
                                                   backupCount=5)
    logger.addHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    # parse command line options
    global options
    options = parse_command_line()

    # use default config file (config.py) or a given file in directory
    # where this file lies
    try:
        if not options.config_file:
            from bbss import config
        else:
            import os.path
            import imp
            comfig_module_name = os.path.splitext(os.path.split(options.config_file)[1])[0]
            f, filename, description = imp.find_module(comfig_module_name)
            config = imp.load_module(comfig_module_name, f, filename,
                                     description)
    except ImportError:
        logger.error("Could not load config file.")
        exit()

    # evaluate given command line options
    if 'format_choice' in options:
        if options.format_choice == 'csv':
            # read file into list of students
            # TODO use options.dontReplaceClassNames when importing
            bbss.read_csv_file(options.filename_import)
            if not options.dontStoreInDB:
                # store newly imported student list in database
                bbss.store_students_db(options.filename_import)
        if options.format_choice == 'excel':
            logger.error('Import from excel files is not yet supported!')
        if options.format_choice == 'logodidact':
            # write csv file for use in logodidact
            logger.info("Exporting student data for use in logodidact...")
            bbss.output_csv_file(options.filename_export)
            logger.info("Exported student data for use in logodidact.")
        if options.format_choice == 'ad':
            logger.error('Export into active directory is not yet supported!')
