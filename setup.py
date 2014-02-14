
from cx_Freeze import setup, Executable
#try:
#    from setuptools.core import setup
#except ImportError:
#    from distutils.core import setup


# Dependencies are automatically detected, but it might need fine tuning.
buildOptions = dict(packages = [], excludes = [])

executables = [
    Executable('bbss_cli.py', 'Console')
]

setup(
    name='bbss - BBS student management',
    version='0.1',
    author='Christian Wichmann',
    author_email='wichmann@bbs-os-brinkstr.de',
    packages=['bbss'],
    url='',
    license='LICENSE',
    description='Management software for students of german vocational colleges.',
    test_suite='bbss.tests.get_suite'
    options = dict(build_exe = buildOptions),
    executables = executables
)
