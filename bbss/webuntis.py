
"""
bbss - BBS Student Management

Exports student data for use with WebUntis.

Created on Fri Jul 21 11:26:47 2017

@author: Christian Wichmann
"""


import csv
import os
import logging
import datetime

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from bbss import data


__all__ = ['export_data']


logger = logging.getLogger('bbss.webuntis')


PAGE_WIDTH, PAGE_HEIGHT = A4
BORDER_HORIZONTAL = 2.0*cm
BORDER_VERTICAL = 1.5*cm
TODAY = datetime.datetime.today().strftime('%d.%m.%Y')
TITLE = 'Benutzerdaten für WebUntis - Import vom {}'.format(TODAY)
AUTHOR = 'bbss - BBS Student Management'


def export_data(output_file, change_set):
    list_of_passwords = _write_class_list_file(output_file, change_set)
    # create a PDF file with every new class including its password
    output_file += '.pdf'
    create_pdf_doc(output_file, list_of_passwords)


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
        logger.warn('Output file already exists, will be overwritten...')
    with open(output_file, 'w', newline='', encoding='utf8') as csvfile:
        output_file_writer = csv.writer(csvfile, delimiter=',')
        output_file_writer.writerow(('Klassenname', 'Kurzname', 'Passwort', 'Personenrolle', 'Benutzergruppe'))
        for c in change_set.classes_added:
            new_password = data.generate_good_password()
            list_of_passwords[c] = new_password
            output_file_writer.writerow((c, c, new_password, 'Klasse', 'Klassen'))
    return list_of_passwords


def create_first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 16)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-58, TITLE)
    canvas.setFont('Helvetica', 10)
    canvas.drawString(BORDER_HORIZONTAL, BORDER_VERTICAL, TITLE)
    canvas.drawRightString(PAGE_WIDTH-BORDER_HORIZONTAL , BORDER_VERTICAL, "Seite 1")
    canvas.restoreState()


def create_later_pages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 10)
    canvas.drawString(BORDER_HORIZONTAL, BORDER_VERTICAL, TITLE)
    canvas.drawRightString(PAGE_WIDTH-BORDER_HORIZONTAL, BORDER_VERTICAL, "Seite {}".format(doc.page))
    canvas.restoreState()


def create_pdf_doc(output_file, list_of_passwords):
    # log all new passwords
    logger.debug('Creating new passwords for classes to be imported into WebUntis...')
    for k, v in list_of_passwords.items():
        logger.debug('User: {} Password: {}'.format(k, v))
    logger.debug('Finished creating new passwords for WebUntis.')
    # create PDF file
    doc = SimpleDocTemplate(output_file, author=AUTHOR, title=TITLE)
    story = [Spacer(1,0.75*cm)]
    data = [('Benutzername: {}'.format(k),'Passwort: {}'.format(v)) for k, v in sorted(list_of_passwords.items())]
    t = Table(data)
    t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica'),
                           ('FONTSIZE',(0,0),(-1,-1), 12),
                           ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                           ('ALIGN',(0,0),(-1,-1),'LEFT'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ('LEFTPADDING', (0,0), (-1,-1), 25),
                           ('RIGHTPADDING', (0,0), (-1,-1), 25),
                           ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                           ('TOPPADDING', (0,0), (-1,-1), 10)]))
    story.append(t)
    doc.build(story, onFirstPage=create_first_page, onLaterPages=create_later_pages)
    # print created PDF file
    #
