bbss - BBS Student Management
=============================

DESCRIPTION
-----------
A tool to store and manage student data.


USAGE
-----

  bbss_cli clear
  bbss_cli import <IMPORT_FILENAME> [--import-format (csv | excel)] [-c CONFIG_FILE] [--dsdb]
  bbss_cli export <EXPORT_FILENAME> [--export-format (logodidact | ad)] [--drc] [--dric]
  bbss_cli search <SEARCH_STRING>

Options:
  -h, --help            Show this help message and exit.
  --version             Show version information.
  --import-format       Import file format for student data. [default: csv]
  --export-format       Export file format for student data. [default: logodidact]
  -c CONFIG_FILE --config CONFIG_FILE
                        Config file in local directory.
  --drc                  Do not replace class names.
  --dric                 Do not replace illegal characters in student names.
  --dsdb                 Do not store imported student data in database.


LICENSE
-------
bbss is released under the GNU General Public License v2 or newer.


REQUIREMENTS
------------
bbss requires Python 3.


PROBLEMS
--------

