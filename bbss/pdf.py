
"""
bbss - BBS Student Management

Exports student data as PDF file to be distributed.

Created on Mon Apr 15 10:51:47 2019

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


logger = logging.getLogger('bbss.pdf')


PAGE_WIDTH, PAGE_HEIGHT = A4
BORDER_HORIZONTAL = 2.0*cm
BORDER_VERTICAL = 1.5*cm
TODAY = datetime.datetime.today().strftime('%d.%m.%Y')
TITLE = 'Benutzerdaten für Logodidact und Moodle (Stand: {})'.format(TODAY)
AUTHOR = 'bbss - BBS Student Management'


def export_data(output_file, student_list):
    # create a PDF file with students from list
    create_pdf_doc(output_file, student_list)


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


def create_pdf_doc(output_file, students_added):
    logger.debug('Exporting students to PDF file...')
    # create PDF file
    main_paragraph_style = ParagraphStyle(name='Normal', fontSize=14, leading=18) #fontName='Inconsolata'
    link_paragraph_style = ParagraphStyle(name='Normal', fontSize=11) #fontName='Inconsolata'
    doc = SimpleDocTemplate(output_file, author=AUTHOR, title=TITLE)
    story = [Spacer(1,0.5*cm)]
	# add page header
    story.append(Paragraph('Bitte die Benutzerdaten an die Schülerinnen und Schüler weitergeben. Danke!', link_paragraph_style))
    story.append(Spacer(1, 0.5*cm))
    for s in sorted(students_added):
        # build inner table with class specific user account information
        inner_table_data = [['Benutzername: {}'.format(s.user_id), 'Passwort: {}'.format(s.password)]]
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
        data = [[Paragraph('Benutzerdaten für {} {} aus der {}:'.format(s.firstname, s.surname, s.classname), link_paragraph_style)],
                [inner_table]]
        outer_table = Table(data)
        outer_table.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica'),
                                         ('FONTSIZE',(0,0),(-1,-1), 14),
                                         ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                         ('ALIGN',(0,0),(-1,-1),'LEFT'),
                                         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.white),
                                         ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                         ('LEFTPADDING', (0,0), (-1,-1), 15),
                                         ('RIGHTPADDING', (0,0), (-1,-1), 15),
                                         ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                                         ('TOPPADDING', (0,0), (-1,-1), 8)]))
        # append outer table for this class to document (without breaking table over multiple pages)
        story.append(KeepTogether(outer_table))
        story.append(Paragraph('<br/><br/>', ParagraphStyle(name='Normal')))
    doc.build(story, onFirstPage=create_first_page, onLaterPages=create_later_pages)
