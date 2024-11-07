
"""
bbss - BBS Student Management

Exports student data for use with WebUntis.

Created on Fri Jul 21 11:26:47 2017

@author: Christian Wichmann
"""


import io
import os
import csv
import logging
import datetime
from itertools import chain

import qrcode
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import KeepTogether, Image

from bbss import data
from bbss import config


__all__ = ['export_data']


logger = logging.getLogger('bbss.webuntis')


PAGE_WIDTH, PAGE_HEIGHT = A4
BORDER_HORIZONTAL = 2.0*cm
BORDER_VERTICAL = 1.5*cm
TODAY = datetime.datetime.today().strftime('%d.%m.%Y')
TITLE = 'Benutzerdaten für WebUntis - Import vom {}'.format(TODAY)
AUTHOR = 'bbss - BBS Student Management'
INCLUDE_QR_CODE = False


def export_data(output_file, change_set):
    # generate import file for importing users for all students
    _write_student_user_list_file(output_file, change_set)
    # generate import file for importing students into base data (Stammdaten)
    _write_student_list_file(output_file, change_set)
    list_of_passwords = _write_class_list_file(output_file, change_set)
    # create a PDF file with every new class including its password
    output_file += '.pdf'
    create_pdf_doc(output_file, list_of_passwords)


def _write_student_list_file(output_file, change_set):
    """
    Write all added and changed students into a CSV file to be imported into
    Webuntis. Removed students will not be updated in Webuntis, the exit date
    should be set manually by the teachers.
    """
    blacklist = ['BFS0X', 'ZABI0X', 'AAK31']
    output_file = os.path.splitext(output_file)
    output_file_students = '{}.students_added{}'.format(*output_file)
    if os.path.exists(output_file_students):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file_students, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Familienname', 'Vorname', 'Geburtsdatum', 'Kurzname', 'Klasse',
                                     'Schlüssel (extern)', 'Eintrittsdatum', 'Austrittsdatum'))
        for student in sorted(change_set.students_added):
            if student.classname in blacklist:
                continue
            # output student data for change set into file
            user_id = student.generate_user_id().lower()
            birthday = datetime.datetime.strptime(student.birthday, '%Y-%m-%d').strftime('%d.%m.%Y')
            # add new student with entry date, so that he/she will not be shown for dates before that!
            output_file_writer.writerow((student.surname, student.firstname,
                                         birthday, user_id, student.classname,
                                         student.guid, datetime.date.today().strftime('%d.%m.%Y'),''))
    # put students that changed classes into separate file because their entry date should not be changed!
    output_file_students = '{}.students_changed{}'.format(*output_file)
    if os.path.exists(output_file_students):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file_students, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Familienname', 'Vorname', 'Geburtsdatum', 'Kurzname', 'Klasse',
                                     'Schlüssel (extern)',  'Austrittsdatum'))
        for student in sorted(change_set.students_changed):
            if student.classname in blacklist:
                continue
            # output student data for change set into file
            user_id = student.generate_user_id().lower()
            birthday = datetime.datetime.strptime(student.birthday, '%Y-%m-%d').strftime('%d.%m.%Y')
            # add changed student without entry date, because that would overwrite an existing date;
            # class change will take effect depending on the given date for that when importing the data!
            output_file_writer.writerow((student.surname, student.firstname,
                                         birthday, user_id, student.classname, student.guid, ''))
    # only export removed students if config option is set, otherwise ignore them
    if config.SHOULD_SET_REMOVE_DATE_FROM_WEBUNTIS:
        output_file_students = '{}.students_removed{}'.format(*output_file)
        if os.path.exists(output_file_students):
            logger.warning('Output file already exists, will be overwritten...')
        with open(output_file_students, 'w', newline='', encoding='utf8') as csvfile:
            output_file_writer = csv.writer(csvfile, delimiter=';')
            output_file_writer.writerow(('Familienname', 'Vorname', 'Geburtsdatum', 'Kurzname', 'Klasse',
                                        'Schlüssel (extern)', 'Austrittsdatum'))
            for student in sorted(change_set.students_removed):
                if student.classname in blacklist:
                    continue
                # output student data for change set into file
                user_id = student.generate_user_id().lower()
                birthday = datetime.datetime.strptime(student.birthday, '%Y-%m-%d').strftime('%d.%m.%Y')
                # add changed student without entry date, because that would overwrite an existing date;
                # class change will take effect depending on the given date for that when importing the data!
                output_file_writer.writerow((student.surname, student.firstname, birthday, user_id,
                                             student.classname, student.guid, datetime.date.today().strftime('%d.%m.%Y')))


def _write_class_list_file(output_file, change_set):
    """
    Writes a file containing all data to import new classes into WebUntis. For
    each new class between the given imports, a new user will be created.
    Classes that are no longer in the database will not be deleted automatically.

    :param output_file: file name to write class list to
    :param change_set: object representing all changes between given imports
    """
    list_of_passwords = {}
    if os.path.exists(output_file):
        logger.warning('Output file already exists, will be overwritten...')
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=',')
        output_file_writer.writerow(('Klassenname', 'Kurzname', 'Passwort', 'Personenrolle', 'Benutzergruppe'))
        for c in change_set.classes_added:
            new_password = data.generate_good_readable_password()
            list_of_passwords[c] = new_password
            output_file_writer.writerow((c, c, new_password, 'Klasse', 'Klassen'))
    # write file with classes that can be deleted from WebUntis (does not work automatically!)
    output_file = os.path.splitext(output_file)
    output_file = '{}.removed{}'.format(*output_file)
    with open(output_file, 'w', newline='', encoding='utf8') as removedlistfile:
        removedlistfile.write('Bitte die folgenden Klassen manuell in WebUntis löschen!\n\n')
        for c in change_set.classes_removed:
            removedlistfile.write(' - {}\n'.format(c))
    return list_of_passwords


def _write_student_user_list_file(output_file, change_set):
    """
    Writes a file containing all data to import new student users into WebUntis.
    Each student will be imported into the base data ("Stammdaten") and gets a
    user for accessing the schedule. This function ONLY produces the user data!

    :param output_file: file name to write student user list to
    :param change_set: object representing all changes between given imports
    """
    output_file = os.path.splitext(output_file)
    output_file_students = '{}.student_users{}'.format(*output_file)
    if os.path.exists(output_file_students):
        logger.warning('Output file already exists, will be overwritten...')
    # export file with all student users
    with open(output_file_students, 'w', newline='', encoding='utf8') as csvfile:
        count = 0
        output_file_writer = csv.writer(csvfile, delimiter=';')
        output_file_writer.writerow(('Klassenname', 'Kurzname', 'Passwort', 'Personenrolle',
                                     'Benutzergruppe', 'Schlüssel (extern)', 'E-Mail Adresse'))
        for student in sorted(chain(change_set.students_added, change_set.students_changed)):
            output_file_writer.writerow((student.classname, student.user_id.lower(),
                                         student.password, 'Schüler*innen', 'Schüler',
                                         student.guid, student.email))
            count += 1
        logger.debug('{0} students (added) exported to Moodle file format.'.format(count))


def create_first_page(canvas, _):
    canvas.saveState()
    canvas.setFont('Helvetica', 16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-58, TITLE)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(BORDER_HORIZONTAL, BORDER_VERTICAL, TITLE)
    canvas.drawRightString(PAGE_WIDTH-BORDER_HORIZONTAL, BORDER_VERTICAL, "Seite 1")
    canvas.restoreState()


def create_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 10)
    canvas.drawString(BORDER_HORIZONTAL, BORDER_VERTICAL, TITLE)
    canvas.drawRightString(PAGE_WIDTH-BORDER_HORIZONTAL, BORDER_VERTICAL, "Seite {}".format(doc.page))
    canvas.restoreState()


def create_qr_code(user, password):
    url_template = 'untis://setschool?url=asopo.webuntis.com&school=BBS Brinkstr-Osnabrück&user={}&key={}&schoolNumber=2042600'
    img = qrcode.make(url_template.format(user, password))
    # get binary data for image to be inserted into PDF
    output = io.BytesIO()
    img.save(output, format=img.format)
    return output


def create_pdf_doc(output_file, list_of_passwords):
    # log all new passwords
    logger.debug('Creating new passwords for classes to be imported into WebUntis...')
    for k, v in list_of_passwords.items():
        logger.debug('User: {} Password: {}'.format(k, v))
    logger.debug('Finished creating new passwords for WebUntis.')
    # create PDF file
    main_paragraph_style = ParagraphStyle(name='Normal', fontSize=14, leading=18)
    link_paragraph_style = ParagraphStyle(name='Normal', fontSize=11)
    doc = SimpleDocTemplate(output_file, author=AUTHOR, title=TITLE)
    story = [Spacer(1, 0.75*cm)]
    for k, v in sorted(list_of_passwords.items()):
        # build inner table with class specific user account information
        img = create_qr_code(k, v)
        if INCLUDE_QR_CODE:
            inner_table_data = [['Benutzername: {}'.format(k), Image(img, width=2.5*cm, height=2.5*cm, hAlign='RIGHT')], ['Passwort: {}'.format(v)]]
            inner_table = Table(inner_table_data, colWidths=[8*cm, 4*cm])
        else:
            inner_table_data = [['Benutzername: {}'.format(k), 'Passwort: {}'.format(v)]]
            inner_table = Table(inner_table_data)
        inner_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Courier'),
                                         ('FONTSIZE', (0, 0), (-1, -1), 12),
                                         ('SPAN', (1, 0), (1, -1)),
                                         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                         ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                                         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
                                         ('BOX', (0, 0), (-1, -1), 0.25, colors.white),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 15),
                                         ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                                         ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                                         ('TOPPADDING', (0, 0), (-1, -1), 5)]))
        # build paragraphs for outer table
        elements = [[Paragraph('Benutzerdaten für den Zugriff auf den Stundenplan<br/>der Klasse {}'.format(k), main_paragraph_style)],
                    [inner_table],
                    [Paragraph('Bitte die Benutzerdaten an die Klasse weitergeben. Danke!', main_paragraph_style)],
                    [Paragraph('Zugriff online unter: https://asopo.webuntis.com/WebUntis/ oder als App: Untis Mobile (Schulname: BBS Brinkstr-Osnabrück)', link_paragraph_style)]]
        outer_table = Table(elements)
        outer_table.setStyle(TableStyle([('FONT', (0, 0), (-1, -1), 'Helvetica'),
                                         ('FONTSIZE', (0, 0), (-1, -1), 14),
                                         ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                         ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                         ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
                                         ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                                         ('LEFTPADDING', (0, 0), (-1, -1), 20),
                                         ('RIGHTPADDING', (0, 0), (-1, -1), 20),
                                         ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                                         ('TOPPADDING', (0, 0), (-1, -1), 10)]))
        # append outer table for this class to document (without breaking table over multiple pages)
        story.append(KeepTogether(outer_table))
        story.append(Paragraph('<br/><br/><br/><br/>', ParagraphStyle(name='Normal')))
    doc.build(story, onFirstPage=create_first_page, onLaterPages=create_later_pages)
