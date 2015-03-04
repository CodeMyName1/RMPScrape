#!/usr/bin/env python

from distutils.core import setup

setup(name='WebScrape',
      version='0.1.2',
      description='A tool for data mining, tailored for RateMyProfessors.com',
      author='Nick Rebhun',
      author_email='nrfactor@gmail.com',
      url='https://www.nrebhun.com',
      packages=['beautifulsoup4', 'sqlite3'],
    )
