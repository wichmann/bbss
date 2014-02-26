#! /usr/bin/env python3

"""
bbss - BBS Student Management

Command line interface for bbss.

Python dependencies:
 - docopt
 - win32com (for Active Directory export)
 -

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

import logging
import logging.handlers
import sys
from docopt import docopt

from bbss import bbss


if __name__ == '__main__':
    # create logger for this application
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss')
    logger.setLevel(logging.DEBUG)
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                       maxBytes=262144,
                                                       backupCount=5)
    log_to_file.setLevel(logging.DEBUG)
    logger.addHandler(log_to_file)
    log_to_screen = logging.StreamHandler(sys.stdout)
    log_to_screen.setLevel(logging.INFO)
    logger.addHandler(log_to_screen)

    # parse command line options
    docopt_string = """
bbss - BBS Student Management - A tool to store and manage student data

Usage:
  bbss_cli clear
  bbss_cli import <IMPORT_FILENAME> [--import-format (csv | excel)] [-c CONFIG_FILE] [--dsdb]
  bbss_cli export <EXPORT_FILENAME> [--export-format (logodidact | radius | ad)] [--drc] [--dric]
  bbss_cli search <SEARCH_STRING>

Options:
  -h, --help            Show this help message and exit.
  --version             Show version information.
  --import-format       Import file format for student data. [default: csv]
  --export-format       Export file format for student data. [default: logodidact]
  -c CONFIG_FILE --config CONFIG_FILE
                        Config file in local directory.
  --drc                  Do not replace class names.
  --dric                 Do not replace illegal characters in student names.
  --dsdb                 Do not store imported student data in database.
"""
    options = docopt(docopt_string, version='bbss 0.0.1')

    # use default config file (config.py) or a given file in directory
    # where this file lies
    #try:
    #    if options['--config'] is None:
    #        from bbss import config
    #    else:
    #        logger.error('Use of config files other than the default not yet implemented.')
    #        import os.path
    #        import imp
    #        config_module_name = os.path.splitext(os.path.split(options['--config'])[1])[0]
    #        f, filename, description = imp.find_module(config_module_name)
    #        config = imp.load_module(config_module_name, f, filename,
    #                                 description)
    #except ImportError:
    #    logger.error("Could not load config file.")
    #    exit()

    # clear database
    if options['clear']:
        logger.info('Deleted database file.')
        bbss.clear_database()

    # search in student database
    elif options['search']:
        logger.info('Searching for student...')
        l = bbss.search_student_in_database(options['<SEARCH_STRING>'])
        if l:
            print('{:>18} {:>18} {:>12} {:>12}'
                  .format('Surname', 'First name', 'Class', 'Birthday'))
            for s in l:
                print('{:>18} {:>18} {:>12} {:>12}'
                      .format(s.surname, s.firstname, s.classname, s.birthday))
        print('{0} students found.'.format(len(l)))

    # evaluate import command line options
    elif options['import']:
        if not options['csv'] and not options['excel']:
            options['csv'] = True
        if options['csv']:
            # read file into list of students
            # TODO use options.dontReplaceClassNames when importing
            bbss.import_csv_file(options['<IMPORT_FILENAME>'])
        elif options['excel']:
            bbss.import_excel_file(options['<IMPORT_FILENAME>'])
        # store newly imported student list in database
        if not options['--dsdb']:
            bbss.store_students_db(options['<IMPORT_FILENAME>'])

    # evaluate import and export command line options
    elif options['export']:
        if not options['logodidact'] and not options['ad'] and not options['radius']:
            options['logodidact'] = True
        if options['logodidact']:
            logger.info("Exporting student data for use in logodidact...")
            bbss.export_csv_file(options['<EXPORT_FILENAME>'],
                                 not options['--dric'])
            logger.info("Exported student data for use in logodidact.")
        elif options['ad']:
            logger.error('Export into active directory is not yet supported!')
        elif options['radius']:
            logger.info("Exporting student data for use in radius server...")
            bbss.export_radius_file(options['<EXPORT_FILENAME>'],
                                    not options['--dric'])
            logger.info("Exported student data for use in radius server.")
