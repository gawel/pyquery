#
# Copyright (C) 2008 - Olivier Lauzanne <olauzanne@gmail.com>
#
# Distributed under the BSD license, see LICENSE.txt

import os

from setuptools import find_packages, setup

install_requires = [
    'lxml>=2.1',
    'cssselect>=1.5.0',
]


def read(*names):
    values = {}
    for name in names:
        filename = name + '.rst'
        if os.path.isfile(filename):
            fd = open(filename)  # NOQA
            value = fd.read()
            fd.close()
        else:
            value = ''
        values[name] = value
    return values


long_description = """
{README}

See http://pyquery.rtfd.org/ for the full documentation

News
====

{CHANGES}

""".format(**read('README', 'CHANGES'))

version = '2.1.0'

setup(name='pyquery',
      version=version,
      description='A jquery-like library for python',
      long_description=long_description,
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 5 - Production/Stable",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
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
      extras_require={
          'test': ['requests', 'webob', 'webtest', 'pytest', 'pytest-cov'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
