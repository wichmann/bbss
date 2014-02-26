
"""
bbss - BBS Student Management

Exports student data for FreeRadius server configuration.

Created on Mon Feb  26 15:08:56 2014

@author: Christian Wichmann
"""


import logging
import os

#from bbss import data


__all__ = ['export_data']


logger = logging.getLogger('bbss.radius')


def export_data(output_file, change_set, replace_illegal_characters=True):
    if os.path.exists(output_file):
        logger.warn('Output file already exists, will be overwritten...')
    with open(output_file, 'w') as export_file:
        for student in change_set.students_added:
            line = '"{0}"\t\tCleartext-Password := "{1}"\n'.format(student.generate_user_id(),
                                                                   student.generate_password())
            export_file.write(line)
