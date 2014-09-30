#!/usr/bin/env python
from distutils.core import setup

from safep import (
    __version__ as version,
    __author__ as author,
    __email__ as author_email)


setup(name='safep',
      version=version,
      description='CLI Password manager',
      author=author,
      author_email=author_email,
      url='https://github.com/miphreal/safep/',
      packages=['safep'],
      scripts=['scripts/safep'],
      install_requires=[
          'pycrypto',
      ],
 )