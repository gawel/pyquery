#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

from setuptools import setup, find_packages
import sys, os

def read(*names):
    values = dict()
    for name in names:
        filename = name+'.txt'
        if os.path.isfile(filename):
            value = open(name+'.txt').read()
        else:
            value = ''
        values[name] = value
    return values

long_description="""
%(README)s

See http://packages.python.org/pyquery/ for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

version = '0.6.1'

setup(name='pyquery',
      version=version,
      description='A jquery-like library for python',
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='jquery html xml',
      author='Olivier Lauzanne',
      author_email='olauzanne@gmail.com',
      url='http://www.bitbucket.org/olauzanne/pyquery/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml>=2.1'
          # -*- Extra requirements: -*-
      ],
      test_requires=['nose'],
      test_suite='nose.collector',
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
