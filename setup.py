##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for zope.app.catalog package

$Id$
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name = 'zope.app.catalog',
      version = '3.7.0dev',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Cataloging and Indexing Framework',
      long_description=(
          read('README.txt')
          + '\n\n' +
          'Detailed Documentation\n'
          '**********************\n'
          + '\n\n' +
          read('src', 'zope', 'app', 'catalog', 'README.txt')
          + '\n\n' +
          read('src', 'zope', 'app', 'catalog', 'event.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope3 catalog index",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.app.catalog',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      extras_require = dict(
          test=['zope.testing',
                'zope.app.component',
                'zope.app.testing',
                'zope.app.securitypolicy',
                'zope.app.zcmlfiles',
                'zope.app.zptpage',
                ]),
      install_requires = [
          'setuptools',
          'ZODB3',
          'zope.annotation',
          'zope.app.intid',
          'zope.component',
          'zope.container',
          'zope.index>=3.5.0',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.location',
          'zope.schema',
          'zope.traversing',
          ],
      include_package_data = True,
      zip_safe = False,
      )
