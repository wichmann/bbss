#! /usr/bin/env python3

"""
bbss - BBS Student Management

Command line interface for bbss.

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
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                   maxBytes=262144,
                                                   backupCount=5)
    logger.addHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)

    # parse command line options
    docopt_string = """
bbss - BBS Student Management - A tool to store and manage student data

Usage:
  bbss_cli clear
  bbss_cli import <IMPORT_FILENAME> [--import-format (csv | excel)] [-c CONFIG_FILE] [--dsdb]
  bbss_cli export <EXPORT_FILENAME> [--export-format (logodidact | ad)] [--drc] [--dric]

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

    # evaluate given command line options
    if options['import']:
        if not options['csv'] and not options['excel']:
            options['csv'] = True
        if options['csv']:
            # read file into list of students
            # TODO use options.dontReplaceClassNames when importing
            bbss.read_csv_file(options['<IMPORT_FILENAME>'])
            if not options['--dsdb']:
                # store newly imported student list in database
                bbss.store_students_db(options['<IMPORT_FILENAME>'])
        if options['excel']:
            logger.error('Import from excel files is not yet supported!')
    if options['export']:
        if not options['logodidact'] and not options['ad']:
            options['logodidact'] = True
        if options['logodidact']:
            # write csv file for use in logodidact
            logger.info("Exporting student data for use in logodidact...")
            bbss.output_csv_file(options['<EXPORT_FILENAME>'],
                                 not options['--dric'])
            logger.info("Exported student data for use in logodidact.")
        if options['ad']:
            logger.error('Export into active directory is not yet supported!')
