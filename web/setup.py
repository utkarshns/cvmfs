#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
  name='django-cvmfs-monitor',
  version='0.1.0',
  url='http://cernvm.cern.ch',
  author='Rene Meusel',
  author_email='rene.meusel@cern.ch',
  license='(c) 2014 CERN - BSD License',
  description='Web Application to Monitor the State of CernVM-FS CDNs.',
  long_description=open('README').read(),
  classifiers= [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    'Topic :: System :: Monitoring',
    'Topic :: System :: Filesystems',
    'Topic :: System :: Networking :: Monitoring',
    'Topic :: System :: Systems Administration'
  ],
  packages=find_packages(),
  install_requires=[ # don't forget to adapt the matching RPM dependencies!
    'cvmfsutils >= 0.1.0',
    'Django >= 1.4',
    'South >= 0.7.5'
  ]
)
