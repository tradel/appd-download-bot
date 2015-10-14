#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

# __author__ = 'Todd Radel <tradel@appdynamics.com>'

from setuptools import setup
import io
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(name='AppDynamicsDownloader',
      version='0.1.8',
      description='AppDynamics Download Robot',
      long_description=read('README.rst'),
      author='Todd Radel',
      author_email='tradel@appdynamics.com',
      url='https://github.com/tradel/appd-download-bot',
      platforms='any',
      scripts=['scripts/download-appdynamics'],
      packages=['appd', 'appd.download'],
      package_data={'': ['README.rst']},
      install_requires=['argparse', 'beautifulsoup4', 'mechanize'],
      extras_require={'testing': ['nose']},
      test_suite='nose.collector',
      tests_require=['nose'],
      license='Apache',
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Development Status :: 4 - Beta',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: System :: Monitoring',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'],
)
