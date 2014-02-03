
"""
bbss - BBS Student Management

Export module for generating data to be used in Microsoft Active Directory.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""


import logging


logger = logging.getLogger('bbss.ad')


LDAP_SERVER = 'ldaps://dc.host.com'
USER_BASE = 'ou=Schueler,ou=BBSBS,DC=SN,DC=BBSBS,DC=LOCAL'


def setup_ad():
    """Set all user accounts for students in AD."""
    logger.info('Setting up ad...')
    logger.info('AD set up.')


def generateOU(class_name, class_determinator, department):
    s = 'ou=' + class_name + ','
    s += 'ou=' + class_determinator + ','
    s += 'ou=' + department + ',' + USER_BASE
    return s
