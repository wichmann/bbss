# bbss - BBS Student Management

## Description

bbss is management software for students of German vocational colleges.

## Usage

bbss can be used either with a graphical user interface or a command line interface.

To start the GUI:

```bash
python bbss_gui.py
```

Command line interface examples:

```bash
python bbss_cli.py clear
python bbss_cli.py import <IMPORT_FILENAME> [--import-format (csv | excel)] [-c CONFIG_FILE] [--dsdb]
python bbss_cli.py export <EXPORT_FILENAME> [--export-format (logodidact | ad)] [--drc] [--dric]
python bbss_cli.py search <SEARCH_STRING>
```

CLI options:

- `-h`, `--help`: Show help and exit.
- `--version`: Show version information.
- `--import-format`: Import file format for student data. Default: `csv`.
- `--export-format`: Export file format for student data. Default: `logodidact`.
- `-c CONFIG_FILE`, `--config CONFIG_FILE`: Config file in local directory.
- `--drc`: Do not replace class names.
- `--dric`: Do not replace illegal characters in student names.
- `--dsdb`: Do not store imported student data in database.

## CSV Converter Script

The repository includes a helper script to convert user CSV data from the iServ source format to an import format used for Moodle:

- Source columns: `Nachname,Vorname,Klasse/Information,Account,Passwort`
- Target columns: `lastname;firstname;cohort1;username;email;password`

Notes:

- Output is semicolon-delimited.
- If `Passwort` is empty, a random password is generated.
- `email` is generated as `username@bbs-brinkstrasse.net` by default.

Run it like this:

```bash
python convert_user_csv.py input.csv output.csv
```

Optional arguments:

```bash
python convert_user_csv.py input.csv output.csv --domain bbs-brinkstrasse.net --password-length 24
```

## Distribution

For easy distribution it is possible to build a single zip or exe file containing all necessary files with either cx_freeze or pyinstaller.

Install tools:

```bash
pip install pyinstaller
pip install cx_freeze
```

Build examples:

```bash
pyinstaller bbss_gui.py
pyinstaller --onefile bbss_gui.py
python setup.py build
```

## Known Problems and Bugs

bbss was written for use under Linux and Windows Vista and higher. Under older systems like Windows XP where the default encoding is not UTF-8, problems can occur.

The encoding of data files has to match the default OS encoding (mostly UTF-8).

## License

bbss is released under the GNU General Public License v2 or newer.

## Requirements

bbss requires at least Python 3.2. The following Python packages are necessary:

- xlrd for importing Microsoft Excel files
- PyQt5 for graphical user interface (including pyqt5-dev-tools for pyuic5 tool)
- win32com for using Microsoft Active Directory under Windows
- docopt for handling command line arguments
- reportlab for creating PDF files as password lists for WebUntis user data
