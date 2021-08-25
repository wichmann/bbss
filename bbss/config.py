
"""
bbss - BBS Student Management

Configuration file containing information for blacklisting class names,
translating illegal characters and mapping class names to departments.

Created on Mon Feb  3 15:08:56 2013

@author: Christian Wichmann
"""


# option whether to overwrite username and password at each import
ALWAYS_OVERWRITE_USERNAME_AND_PASSWORD = False


# option whether to import email addresses every time even if the student was already in the database
ALWAYS_IMPORT_EMAIL_ADDRESSES = True


# option whether to set remove date for students, otherwise deleted students will be ignored!
SHOULD_SET_REMOVE_DATE_FROM_WEBUNTIS = False


# black list of classes not to load
class_blacklist = ('OWS', 'OWH')


# map translating all illegal characters into legal (ascii) characters
char_map = {'ä': 'ae',
            'à': 'a',
            'á': 'a',
            'â': 'a',
            'ã': 'a',
            'Ä': 'Ae',
            'À': 'A',
            'Á': 'A',
            'Â': 'A',
            'Ã': 'A',
            'è': 'e',
            'é': 'e',
            'ê': 'e',
            'È': 'E',
            'É': 'E',
            'Ê': 'E',
            'ö': 'oe',
            'ò': 'o',
            'ó': 'o',
            'ô': 'o',
            'õ': 'o',
            'Ö': 'Oe',
            'Ò': 'O',
            'Ó': 'O',
            'Ô': 'O',
            'Õ': 'O',
            'ü': 'ue',
            'ù': 'u',
            'ú': 'u',
            'û': 'u',
            'Ü': 'Ue',
            'Ù': 'U',
            'Ú': 'U',
            'Û': 'U',
            'í': 'i',
            'ß': 'ss',
            'Ç': 'C',
            'ç': 'c',
            'č': 'c',
            'ć': 'c',
            '´': '',
            '-': '',
            ' ': ''}


# map translating class names as used to class names a necessary for generating user names
class_map = {'SGOX': 'SGO',
             'SGSX': 'SGO',
             'STEX': 'STE',
             'CPHY': 'CPWY',
             'MMGX': 'MMG',
             'EIEX': 'EIE',
             'KZMX': 'KZM',
             'MKMX': 'MKM',
             'MAFX': 'MAF',
             'BGT11A': 'BGT',
             'BGT11B': 'BGT',
             'BGT11C': 'BGT',
             'BGT11D': 'BGT',
             'BGT12': 'BGT',
             'BGT13': 'BGT',
             'TG11A': 'TG',
             'TG11B': 'TG',
             'TG11C': 'TG',
             'TG11D': 'TG',
             'TG12': 'TG',
             'TG13': 'TG'}


# map translating a class determinator (without the identifier for a specific class)
# to a department to which this class belongs to
department_map = {('BFSE', 'EIE', 'ELH', 'ELI', 'EIEX'): 'Elektrotechnik',
                  ('BGT', 'BGTA', 'BGTB', 'BGTC', 'BGT12', 'BGT13',
                   'TG', 'TG11A', 'TG11B', 'TG11C', 'TG11D', 'TG12', 'TG13'): 'Berufliches Gymnasium',
                  ('FOSS', 'FOSW', 'FSAE', 'FSAM', 'FSE', 'FSM'): 'Fachschule',
                  ('BFIA', 'IFA', 'IFI', 'ISE'): 'IT-Berufe',
                  ('KBK', 'KFZ', 'KKB', 'KZM', 'KZO', 'KZU', 'KZF'): 'Kraftfahrzeugtechnik',
                  ('FSAME', 'SME'): 'Mechatronik',
                  ('BEKM', 'BFSM', 'MAF', 'MAKM', 'MII', 'MIM', 'MIP', 'MMB', 'MME', 'MMG', 'MPV', 'MTL', 'MWM', 'MZD', 'MZM'): 'Metalltechnik',
                  ('STZ', 'STZH', 'STPS', 'STP', 'STSV', 'STZE', 'STEX'): 'Technische Zeichner',
                  ('CCL', 'CPWY', 'SAO', 'SGO'): 'Sonstige Berufe',
                  ('VAM'): 'Versorgungstechnik',
                  ('IHK', 'ITW'): 'Gäste',
                  ('OWS', 'OWH'): 'Osnabrücker Werkstätten'}


# list containing blicklisted strings when importing mail addresses from BBS-Planung
mail_address_blacklist = ['unbekannt', 'nicht bekannt', 'keine bekannt', 'nicht vorhanden',
                          'keine angabe', 'ohne angabe', 'ohne angaben', 'wird nachgereicht',
                          'keine', 'nicht angegeben', 'k.a.', 'n.n.', 'n.a.', 'o.a.',
                          'keine ahnung', 'ohne', 'ka', './.', 'keine@vorhanden.de',
                          'keine@e-mail', 'noch.nicht@vorhanden.de', 'unbekannt@de']
