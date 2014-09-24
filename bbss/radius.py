
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
        count = 0
        class_of_student = ''
        line = '{:20}\t\tCleartext-Password := "{}"\n'
        for student in sorted(change_set.students_added):
            count += 1
            if class_of_student != student.classname:
                export_file.write('# {}\n'.format(student.classname))
                class_of_student = student.classname
            export_file.write(line.format('"'+student.generate_user_id()+'"',
                                          student.generate_password()))
        logger.debug('{0} students exported to radius file format.'
                     .format(count))
