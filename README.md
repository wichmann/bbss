bbss - BBS Student Management
=============================

DESCRIPTION
-----------
bbss is a management software for students of german vocational colleges.


USAGE
-----
bbss can be used either with a graphical user interface or a command line
interface. To start the GUI, execute
 
    bbss_gui.py
  
Usage of bbss command line interface:

    bbss_cli clear
    bbss_cli import <IMPORT_FILENAME> [--import-format (csv | excel)] [-c CONFIG_FILE] [--dsdb]
    bbss_cli export <EXPORT_FILENAME> [--export-format (logodidact | ad)] [--drc] [--dric]
    bbss_cli search <SEARCH_STRING>

    Options:
    -h, --help             Show this help message and exit.
    --version              Show version information.
    --import-format        Import file format for student data. [default: csv]
    --export-format        Export file format for student data. [default: logodidact]
    -c CONFIG_FILE --config CONFIG_FILE
                           Config file in local directory.
    --drc                  Do not replace class names.
    --dric                 Do not replace illegal characters in student names.
    --dsdb                 Do not store imported student data in database.

For easy distribution it is possible to build a single zip or exe file
containing all necessary files with either cx_freeze or pyinstaller. Both
tools can be installed by using pip:

    pip install pyinstaller
    pip install cx_freeze

After the installation both tools can create in single directory or single
file distribution:

    pyinstaller bbss_gui.py
    pyinstaller --onefile bbss_gui.py
    python setup.py build


KNOWN PROBLEMS AND BUGS
-----------------------
bbss was written for use under Linux and Windows Vista and higher. Under older
systems like Windows XP where the default encoding is not UTF-8 problems can
occur.

The encoding of data files has to match the default OS encoding (mostly UTF-8).


LICENSE
-------
bbss is released under the GNU General Public License v2 or newer.


REQUIREMENTS
------------
bbss requires at least Python 3.2. The following Python packages are necessary:
* xlrd for importing Microsoft Excel files
* PyQt5 for graphical user interface (including pyqt5-dev-tools for pyuic5 tool)
* win32com for using Microsoft Active Directory under Windows
* docopt for handling command line arguments
* reportlab for creating PDF files as pasword lists for WebUntis user data


PROBLEMS
--------

