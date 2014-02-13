
"""
bbss - BBS Student Management

Helper functions for reading data from and storing data in an active
directory.

Created on Mon Feb  3 15:08:56 2014

@author: Christian Wichmann
"""

###
# More information:
# - http://www.selfadsi.de/read.htm
# - http://www.activexperts.com/network-monitor/windowsmanagement/adminscripts/usersgroups/ous/#CreateOU.htm
###


def is_windows():
    #from sys import platform as _platform
    #if _platform == "win32":
    #    return True
    #else:
    #    return False
    import os
    if os.name == 'nt':
        return True
    else:
        return False


def only_on_windows(f):
    if is_windows():
        return f
    else:
        def print_warning(*args):
            print('Active directory can only be used under windows.')
        return print_warning


if is_windows():
    import win32com
    import win32com.client


address_base = 'LDAP://'
domain_controller = 'DC=SN,DC=BBSBS,DC=LOCAL'


@only_on_windows
def add_account(location, account):
    try:
        ad_obj = win32com.client.GetObject(location)
        ad_user = ad_obj.Create('User', 'CN=' + account['login'])
        ad_user.Put('sAMAccountName', account['login'])
        # TODO Set correct 'User Principal Name'
        ad_user.Put('userPrincipalName', account['login'])
        ad_user.Put('DisplayName', account['first'] + ' ' + account['last'])
        ad_user.Put('givenName', account['first'])
        ad_user.Put('sn', account['last'])
        ad_user.Put('description', 'Schueler')
        ad_user.SetInfo()
        #ad_user.GetInfo()
        # TODO Add password for account
        #ad_user.setpassword('asdf')
        #ad_user.Put('pwdLastSet',0) #-- force reset of password
        #ad_user.AccountDisabled = 0
        #ad_user.SetInfo()
        #ad_user.Put('physicalDeliveryOfficeName','office 1')
        #ad_user.Extensionattribute10='your own attribute'
        #ad_user.Put('HomeDirectory',r'\\server1\ '[:-1]+user['login'])
        #ad_user.Put('HomeDrive','H:')
        #ad_user.LoginScript='login.bat'
        #ad_user.SetInfo()
    except:
        print('User already in AD.')


@only_on_windows
def delete_account(location, account_name):
    try:
        ad = win32com.client.GetObject(location)
        ad.Delete('User', 'CN=' + account_name)
    except:
        print('User could not be deleted in AD.')


@only_on_windows
def add_ou(location, ou):
    try:
        ad = win32com.client.GetObject(location)
        new_ou = ad.Create('organizationalUnit', 'OU='+ou)
        new_ou.SetInfo()
    except:
        print('Object already in AD.')


@only_on_windows
def delete_ou(location, ou):
    try:
        ad = win32com.client.GetObject(location)
        ad.Delete('organizationalUnit', 'OU=' + ou)
    except:
        print('OU could not be deleted in AD.')


@only_on_windows
def add_student(list_of_ou, student):
    #address_base = 'LDAP://'
    #domain_controller = 'DC=SN,DC=BBSBS,DC=LOCAL'
    location = ''
    # check for organisational units
    for ou in list_of_ou:
        add_ou(address_base + location + domain_controller, ou)
        # build new location for next ou
        location = 'OU=' + ou + ',' + location
        print(address_base + location)
    # add student to correct ou
    add_account(address_base + location + domain_controller, student)


@only_on_windows
def lookup_account(account_name):
    exists_already = False
    try:
        ad = win32com.client.GetObject(address_base + domain_controller)
        ad.GetInfo()
        user = ad.GetObject('User', 'CN=' + account_name)
        user.GetInfo()
        exists_already = False
    except:
        exists_already = True
    else:
        exists_already = False

    if exists_already:
        print('yes')
    else:
        print('no')


@only_on_windows
def unit_test_2():
    add_student(('BBSBS3', 'Schueler', 'Elektrotechnik', 'ELH', 'ELH01'),
                {'first': 'Bernd', 'last': 'Smith', 'login': 'asdf'})


@only_on_windows
def unit_test_1():
    add_ou(address_base + domain_controller, 'temp1')
    add_account(address_base + 'OU=temp1,' + domain_controller,
                {'first': 'Bernd', 'last': 'Smith', 'login': 'asdf'})
    delete_account(address_base + 'OU=temp1,' + domain_controller, 'asdf')
    delete_ou(address_base + domain_controller, 'temp1')


#lookup_account('asdf') #'tom4441981'
