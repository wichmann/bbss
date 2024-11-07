#! /usr/bin/env python3

"""
Pack a ZIP file with user images for import into Moodle.

@author: Christian Wichmann
"""

import os
import sys
import zipfile
import logging
import logging.handlers

from bbss import bbss


IMAGE_ARCHIVE = 'e:\Schülerfotos\AlleSchueler_2024-08-30.zip'
MOODLE_IMAGES = 'e:\Schülerfotos\Archiv_Moodle_2024-08-30.zip'


def copy_from_zip_to_zip(source_zipfile: os.PathLike, target_zipfile: os.PathLike):
    """
    Source: https://gist.github.com/theriverman/38018f2fbf69fee1daf5dbbf6524431b
    """
    with zipfile.ZipFile(target_zipfile, 'w', compression=zipfile.ZIP_DEFLATED) as target_zip:
        with zipfile.ZipFile(source_zipfile, 'r') as source_zip:
            for userid, username in users:
                try:
                    if 'IFA42' not in username:
                        continue
                    source_zip_filename = f'{userid}.jpg'
                    file_in_source = source_zip.getinfo(source_zip_filename)
                    target_zip_filename = f'{username.lower()}.jpeg'
                    #target_zip.write(zipfile.Path(source_zip, file_in_source.filename), target_zip_filename)
                    target_zip.writestr(target_zip_filename, source_zip.open(file_in_source.filename).read())
                except KeyError:
                    print(f'Keine Bilddatei für ID "{userid}" gefunden!')


if __name__ == '__main__':
    # create logger for this application
    LOG_FILENAME = 'bbss.log'
    logger = logging.getLogger('bbss.imagecollectioncreator')
    logger.setLevel(logging.DEBUG)
    log_to_file = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=262144, backupCount=5, encoding='utf-8')
    log_to_file.setLevel(logging.DEBUG)
    logger.addHandler(log_to_file)
    log_to_screen = logging.StreamHandler(sys.stdout)
    log_to_screen.setLevel(logging.INFO)
    logger.addHandler(log_to_screen)

    users = bbss.get_usernames_and_ids()
    copy_from_zip_to_zip(IMAGE_ARCHIVE, MOODLE_IMAGES)
