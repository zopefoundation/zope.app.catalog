##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
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
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.catalog package

"""
import os

from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


tests_require = [
    'zope.app.appsetup',
    'zope.app.basicskin >= 4.0.0',
    'zope.app.container >= 4.0.0',
    'zope.app.component >= 4.0.0',
    'zope.app.form >= 5.0.0',
    'zope.app.publisher',
    'zope.app.publication',
    'zope.app.schema >= 4.0.0',
    'zope.app.wsgi[testlayer] >= 5.3',

    'zope.browserpage',
    'zope.browserresource',
    'zope.container',
    'zope.formlib',
    'zope.login',
    'zope.principalannotation',
    'zope.principalregistry',
    'zope.publisher',
    'zope.securitypolicy',
    'zope.testbrowser >= 5.2',
    'zope.testing',
    'zope.testrunner >= 6.4',
    'zope.traversing >= 4.1.0',

    'webtest',
]

setup(name='zope.app.catalog',
      version='6.0',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.dev',
      description='Management pages for Zope Catalog',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      keywords="zope3 catalog index",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Programming Language :: Python :: Implementation :: CPython',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      url='http://github.com/zopefoundation/zope.app.catalog',
      license='ZPL-2.1',
      python_requires='>=3.9',
      extras_require={
          'test': tests_require,
      },
      tests_require=tests_require,
      install_requires=[
          'setuptools',
          'zope.catalog >= 4.2.0',
      ],
      include_package_data=True,
      zip_safe=False,
      )
