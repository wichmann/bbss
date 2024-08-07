
"""
bbss - BBS Student Management

Exports student data for FreeRadius server configuration.

Created on Mon Feb  26 15:08:56 2014

@author: Christian Wichmann
"""


import logging
import os
from itertools import chain


__all__ = ['export_data']


logger = logging.getLogger('bbss.radius')


def export_data(output_file, change_set):
    """
    Exports a given change set into a configuration file for a Radius authentication server.
    """
    if os.path.exists(output_file):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file, 'w') as export_file:
        count = 0
        class_of_student = ''
        line = '{:20}\t\tCleartext-Password := "{}"\n'
        last_exported_student = None
        for student in sorted(chain(change_set.students_added, change_set.students_changed),  key=lambda s: s.classname):
            if student == last_exported_student:
                continue
            last_exported_student = student
            count += 1
            if class_of_student != student.classname:
                export_file.write('# {}\n'.format(student.classname))
                class_of_student = student.classname
            formatted_line = line.format(student.generate_user_id().lower(),
                                         student.generate_password())
            export_file.write(formatted_line)
        logger.debug('{0} students exported to radius file format.'
                     .format(count))
