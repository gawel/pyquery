#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

from setuptools import setup, find_packages
import xml.sax.saxutils
import sys, os

def read(filename):
    text = open(filename).read()
    text = unicode(text, 'utf-8').encode('ascii', 'xmlcharrefreplace')
    return xml.sax.saxutils.escape(text)

long_description = read(os.path.join('pyquery', 'README.txt'))

version = '0.2'

setup(name='pyquery',
      version=version,
      description='A jquery-like library for manipulating html and xml documents',
      long_description=long_description,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='jquery html xml',
      author='Olivier Lauzanne',
      author_email='olauzanne@gmail.com',
      url='http://libreamoi.com/index.php/pyquery',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml>=2.1'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
