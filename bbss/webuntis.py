
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
from reportlab.lib.units import cm, mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.flowables import KeepTogether

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
	# write file with classes that can be deleted from WebUntis (does not work automatically!)
    output_file = os.path.splitext(output_file)
    output_file = '{}.removed{}'.format(*output_file)
    with open(output_file, 'w', newline='', encoding='utf8') as removedlistfile:
        removedlistfile.write('Bitte die folgenden Klassen manuell in WebUntis löschen!\n\n')
        for c in change_set.classes_removed:
            removedlistfile.write(' - {}\n'.format(c))
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
    main_paragraph_style = ParagraphStyle(name='Normal', fontSize=14, leading=18) #fontName='Inconsolata'
    link_paragraph_style = ParagraphStyle(name='Normal', fontSize=11) #fontName='Inconsolata'
    doc = SimpleDocTemplate(output_file, author=AUTHOR, title=TITLE)
    story = [Spacer(1,0.75*cm)]
    for k, v in sorted(list_of_passwords.items()):
        # build inner table with class specific user account information
        inner_table_data = [['Benutzername: {}'.format(k), 'Passwort: {}'.format(v)]]
        inner_table = Table(inner_table_data)
        inner_table.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Courier'),
                                         ('FONTSIZE',(0,0),(-1,-1), 12),
                                         ('VALIGN',(0,0),(-1,-1),'TOP'),
                                         ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
                                         ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                                         ('LEFTPADDING', (0,0), (-1,-1), 20),
                                         ('RIGHTPADDING', (0,0), (-1,-1), 20),
                                         ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                                         ('TOPPADDING', (0,0), (-1,-1), 5)]))
        # build paragraphs for outer table
        data = [[Paragraph('Benutzerdaten für den Zugriff auf den Stundenplan<br/>der Klasse {}'.format(k),
                           main_paragraph_style)],
                [inner_table],
                [Paragraph('Online: https://asopo.webuntis.com/WebUntis/ oder als App: Untis Mobile (Schulname: BBS Brinkstr-Osnabrück)',
                           link_paragraph_style)]]
        outer_table = Table(data)
        outer_table.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica'),
                                         ('FONTSIZE',(0,0),(-1,-1), 14),
                                         ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                         ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
                                         ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                         ('LEFTPADDING', (0,0), (-1,-1), 20),
                                         ('RIGHTPADDING', (0,0), (-1,-1), 20),
                                         ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                                         ('TOPPADDING', (0,0), (-1,-1), 10)]))
        # append outer table for this class to document (without breaking table over multiple pages)
        story.append(KeepTogether(outer_table))
        story.append(Paragraph('<br/><br/>', ParagraphStyle(name='Normal')))
    doc.build(story, onFirstPage=create_first_page, onLaterPages=create_later_pages)
