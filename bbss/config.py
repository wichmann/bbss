
"""
bbss - BBS Student Management

Configuration file containing information for blacklisting class names,
translating illegal characters and mapping class names to departments.

Created on Mon Feb  3 15:08:56 2013

@author: Christian Wichmann
"""


### black list of classes not to load
class_blacklist = ('OWS', 'OWH')


### map translating all illegal characters into legal (ascii) characters
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
            'ß': 'ss',
            '´': '',
            '-': '',
            ' ': ''}


### map translating class names as used to class names a necessary for
### generating user names
class_map = {'SGOX': 'SGO',
             'SGSX': 'SGO',
             'STEX': 'STE',
             'CPHY': 'CPWY',
             'MMGX': 'MMG',
             'EIEX': 'EIE',
             'KZMX': 'KZM',
             'MKMX': 'MKM',
             'MAFX': 'MAF'}


### map translating a class determinator (without the identifier for a
### specific class) to a department to which this class belongs to
department_map = {('BFSE', 'EIE', 'ELH', 'ELI', 'EIEX'): 'Elektrotechnik',
                  ('BGT', 'BGTA', 'BGTB', 'BGTC', 'BGT12', 'BGT13'): 'Berufliches Gymnasium',
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
