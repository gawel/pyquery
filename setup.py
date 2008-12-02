from setuptools import setup, find_packages
import sys, os

import pyquery

version = '0.1'

setup(name='pyquery',
      version=version,
      description='A jquery-like library for manipulating html and xml documents',
      long_description=pyquery.__doc__,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='jquery html xml',
      author='Olivier Lauzanne',
      author_email='olauzanne@gmail.com',
      url='http://libreamoi.com/index.php/pyquery',
      license='MIT',
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
