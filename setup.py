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

setup(name = 'zope.app.catalog',
      version = '3.5.0a2',
      url = 'http://svn.zope.org/zope.app.catalog',
      license = 'ZPL 2.1',
      description = 'Zope app.catalog',
      author = 'Zope Corporation and Contributors',
      author_email = 'zope3-dev@zope.org',
      long_description = "",

      packages = find_packages('src'),
      package_dir = {'': 'src'},

      namespace_packages = ['zope', 'zope.app'],
      install_requires = ['setuptools',
                          'ZODB3 >=3.8.0a1.dev-r74780',
                          'zope.annotation',
                          'zope.app.component',
                          'zope.app.container',
                          'zope.app.intid',
                          'zope.app.testing',
                          'zope.component',
                          'zope.index',
                          'zope.interface',
                          'zope.lifecycleevent',
                          'zope.location',
                          'zope.schema',
                          'zope.testing',
                          'zope.traversing',
                          ],
      include_package_data = True,
      extras_require = dict(test=['zope.testing',
                                  'zope.app.testing',
                                  'zope.app.securitypolicy',
                                  'zope.app.zcmlfiles',
                                  'zope.app.zptpage',
                                  ]
                            ),
      zip_safe = False,
      )
