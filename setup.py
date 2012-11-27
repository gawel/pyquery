#-*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

from setuptools import setup, find_packages
import os


def read(*names):
    values = dict()
    for name in names:
        filename = name + '.txt'
        if os.path.isfile(filename):
            fd = open(name + '.txt')
            value = fd.read()
            fd.close()
        else:
            value = ''
        values[name] = value
    return values


long_description = """
%(README)s

See http://packages.python.org/pyquery/ for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

version = '1.2.2'

setup(name='pyquery',
      version=version,
      description='A jquery-like library for python',
      long_description=long_description,
      classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        ],
      keywords='jquery html xml',
      author='Olivier Lauzanne',
      author_email='olauzanne@gmail.com',
      maintainer='Gael Pasgrimaud',
      maintainer_email='gael@gawel.org',
      url='http://www.bitbucket.org/olauzanne/pyquery/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'lxml>=2.1',
          'cssselect',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
