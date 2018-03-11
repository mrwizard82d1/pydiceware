#! env python

from distutils.core import setup

import os

setup(name='pydiceware',
      version='1.0',
      description='Utilities to generate passwords using pydiceware.',
      author='Larry Jones',
      author_email='mrwizard82d1@earthlink.net',
      packages=['pydiceware', ],
      data_files=[('', ['pydiceware/diceware.wordlist.txt',
                        'pydiceware/diceware8k.txt']),])

 
