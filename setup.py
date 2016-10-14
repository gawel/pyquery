# -*- coding:utf-8 -*-
#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

from setuptools import setup, find_packages
import os


install_requires = [
    'lxml>=2.1',
    'cssselect>0.7.9',
]


def read(*names):
    values = dict()
    for name in names:
        filename = name + '.rst'
        if os.path.isfile(filename):
            fd = open(filename)
            value = fd.read()
            fd.close()
        else:
            value = ''
        values[name] = value
    return values


long_description = """
%(README)s

See http://pyquery.rtfd.org/ for the full documentation

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

version = '1.2.16'

setup(name='pyquery',
      version=version,
      description='A jquery-like library for python',
      long_description=long_description,
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ],
      keywords='jquery html xml scraping',
      author='Olivier Lauzanne',
      author_email='olauzanne@gmail.com',
      maintainer='Gael Pasgrimaud',
      maintainer_email='gael@gawel.org',
      url='https://github.com/gawel/pyquery',
      license='BSD',
      packages=find_packages(exclude=[
          'bootstrap', 'bootstrap-py3k', 'docs', 'tests', 'README_fixt'
      ]),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
