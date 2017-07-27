#! /usr/bin/env python3

import sys
from cx_Freeze import setup, Executable


# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages=[], excludes=[])

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('bbss_cli.py'),
    Executable('bbss_gui.py', base=base)
]

setup(
    name='bbss - BBS student management',
    version='0.3',
    author='Christian Wichmann',
    author_email='wichmann@bbs-os-brinkstr.de',
    packages=['bbss', 'gui'],
    url='',
    license='LICENSE',
    description='Management software for students of german vocational colleges',
    #test_suite='bbss.tests.get_suite',
    options=dict(build_exe=buildOptions),
    executables=executables
)
