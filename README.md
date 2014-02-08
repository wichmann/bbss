bbss - BBS Student Management
=============================

DESCRIPTION
-----------
A tool to manage student data...                                                                                                                                  


USAGE
-----

bbss_cli.py [-h] [-c CONFIG_FILE] [-drc] [-dsdb] {import,export} ...                                                                                       
                                                                                                                                                                                                                                                                                                                                
positional arguments:
  {import,export}
    import
    export

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config CONFIG_FILE
                        config file in local directory
  -drc                  defines whether to replace class names
  -dsdb                 defines whether to store imported student data in
                        database

bbss_cli.py import [-h] [-f {csv,excel}] filename_import

bbss_cli.py export [-h] [-f {logodidact,ad}] filename_export


LICENSE
-------
bbss is released under the GNU General Public License v2 or newer.


REQUIREMENTS
------------
bbss requires Python 3.


PROBLEMS
--------

