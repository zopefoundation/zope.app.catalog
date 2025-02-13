=======
CHANGES
=======

5.1 (unreleased)
----------------

- Make tests to be compatible with multipart >= 1.x.


5.0 (2024-11-12)
----------------

- Drop support for Python 2.7, 3.4, 3.5, 3.6, 3.7.

- Drop support for PyPy3 because of breaking tests.

- Add support for Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13.


4.0.0 (2017-05-05)
------------------

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Remove test dependency on ``zope.app.testing`` and
  ``zope.app.zcmlfiles``, among others.


3.8.1 (2010-01-08)
------------------

- Removed unneeded dependencies on zope.app.publisher and zope.app.form, moved
  zope.app.intid to the test dependencies.

- Import hooks functionality from zope.component after it was moved there from
  zope.site. This lifts the test dependency on zope.site.

- Use new zope.publisher that requires zope.login.

3.8.0 (2009-02-01)
------------------

- Move most of this package's code to new ``zope.catalog`` package,
  leaving only ZMI-related views and backward-compatibility imports
  here.

3.7.0 (2009-01-31)
------------------

- Change catalog's addMenuItem permission to zope.ManageServices
  as it doesn't make any sense to add an empty catalog that you
  can't modify with zope.ManageContent permission and it's completely
  useless without indexes. So there's no need to show a menu item.

- Replaced dependency on `zope.app.container` with a lighter-weight
  dependency upon the newly refactored `zope.container` package.

3.6.0 (2009-01-03)
------------------

- Make TextIndex addform use default values as specified in
  zope.app.catalog.text.ITextIndex interface. Also, change
  "searchableText" to "getSearchableText" there, as it's the
  right value.

- Add Keyword (case-insensitive and case-sensitive) catalog
  indices. It's now possible to use them, because ones in
  zope.index now implement IIndexSearch interface.

- Add support for sorting, reversing and limiting result set
  in the ``searchResults`` method, using new IIndexSort interface
  features of zope.index.

3.5.2 (2008-12-28)
------------------

- Remove testing dependencies from install_requires.

3.5.1 (2007-10-31)
------------------

- Resolve ``ZopeSecurityPolicy`` deprecation warning.


3.5.0 (2007-10-11)
------------------

- Updated some meta-data.

- Move ``ftests.py`` to ``tests.py``.


3.5.0a3 (2007-09-27)
--------------------

- removed some deprecations


3.5.0a2 (2007-09-21)
--------------------

- bugfix: passing the context to getAllUtilitiesRegisteredFor in all
  eventhandlers because no catalog was found which was located in a
  sub site and for example the ObjectModifiesEvent get fired from somewhere
  in the root.


3.5.0a1 (2007-06-26)
--------------------

- Added marker interfaces to prevent automatic indexing (see: ``event.txt``)
