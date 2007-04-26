##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for catalog

Note that indexes &c already have test suites, we only have to check that
a catalog passes on events that it receives.

$Id$
"""
import unittest
from zope.testing import doctest

from zope.interface import implements
from zope.interface.verify import verifyObject
from zope.app.testing import ztapi, setup, placelesssetup
from BTrees.IFBTree import IFSet
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import setSite

from zope.index.interfaces import IInjection, IIndexSearch
from zope.app.catalog.interfaces import ICatalog
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.attribute import AttributeIndex
from zope.app.catalog.field import FieldIndex

class ReferenceStub:
    def __init__(self, obj):
        self.obj = obj

    def __call__(self):
        return self.obj


class IntIdsStub:
    """A stub for IntIds."""
    implements(IIntIds)

    def __init__(self):
        self.ids = {}
        self.objs = {}
        self.lastid = 0

    def _generateId(self):
        self.lastid += 1
        return self.lastid

    def register(self, ob):
        if ob not in self.ids:
            uid = self._generateId()
            self.ids[ob] = uid
            self.objs[uid] = ob
            return uid
        else:
            return self.ids[ob]

    def unregister(self, ob):
        uid = self.ids[ob]
        del self.ids[ob]
        del self.objs[id]

    def getObject(self, uid):
        return self.objs[uid]

    def getId(self, ob):
        return self.ids[ob]

    def queryId(self, ob, default=None):
        return self.ids.get(ob, default)

    def __iter__(self):
        return self.objs.iterkeys()


class StubIndex:
    """A stub for Index."""

    implements(IIndexSearch, IInjection)

    def __init__(self, field_name, interface=None):
        self._field_name = field_name
        self.interface = interface
        self.doc = {}

    def index_doc(self, docid, obj):
        self.doc[docid] = obj

    def unindex_doc(self, docid):
        del self.doc[docid]

    def apply(self, term):
        results = []
        for docid in self.doc:
            obj = self.doc[docid]
            fieldname = getattr(obj, self._field_name, '')
            if fieldname == term:
                results.append(docid)
        return IFSet(results)


class stoopid:
    def __init__(self, **kw):
        self.__dict__ = kw


class Test(placelesssetup.PlacelessSetup, unittest.TestCase):

    def test_catalog_add_del_indexes(self):
        catalog = Catalog()
        verifyObject(ICatalog, catalog)
        index = StubIndex('author', None)
        catalog['author'] = index
        self.assertEqual(list(catalog.keys()), ['author'])
        index = StubIndex('title', None)
        catalog['title'] = index
        indexes = list(catalog.keys())
        indexes.sort()
        self.assertEqual(indexes, ['author', 'title'])
        del catalog['author']
        self.assertEqual(list(catalog.keys()), ['title'])

    def _frob_intidutil(self, ints=True, apes=True):
        uidutil = IntIdsStub()
        ztapi.provideUtility(IIntIds, uidutil)
        # whack some objects in our little objecthub
        if ints:
            for i in range(10):
                uidutil.register("<object %s>"%i)
        if apes:
            uidutil.register(stoopid(simiantype='monkey', name='bobo'))
            uidutil.register(stoopid(simiantype='monkey', name='bubbles'))
            uidutil.register(stoopid(simiantype='monkey', name='ginger'))
            uidutil.register(stoopid(simiantype='bonobo', name='ziczac'))
            uidutil.register(stoopid(simiantype='bonobo', name='bobo'))
            uidutil.register(stoopid(simiantype='punyhuman', name='anthony'))
            uidutil.register(stoopid(simiantype='punyhuman', name='andy'))
            uidutil.register(stoopid(simiantype='punyhuman', name='kev'))

    def test_updateindexes(self):
        """Test a full refresh."""
        self._frob_intidutil()
        catalog = Catalog()
        catalog['author'] = StubIndex('author', None)
        catalog['title'] = StubIndex('author', None)
        catalog.updateIndexes()
        for index in catalog.values():
            checkNotifies = index.doc
            self.assertEqual(len(checkNotifies), 18)

    def test_updateindex(self):
        """Test a full refresh."""
        self._frob_intidutil()
        catalog = Catalog()
        catalog['author'] = StubIndex('author', None)
        catalog['title'] = StubIndex('author', None)
        catalog.updateIndex(catalog['author'])
        checkNotifies = catalog['author'].doc
        self.assertEqual(len(checkNotifies), 18)
        checkNotifies = catalog['title'].doc
        self.assertEqual(len(checkNotifies), 0)

    def test_basicsearch(self):
        """Test the simple search results interface."""
        self._frob_intidutil(ints=0)
        catalog = Catalog()
        catalog['simiantype'] = StubIndex('simiantype', None)
        catalog['name'] = StubIndex('name', None)
        catalog.updateIndexes()

        res = catalog.searchResults(simiantype='monkey')
        names = [x.name for x in res]
        names.sort()
        self.assertEqual(len(names), 3)
        self.assertEqual(names, ['bobo', 'bubbles', 'ginger'])

        res = catalog.searchResults(name='bobo')
        names = [x.simiantype for x in res]
        names.sort()
        self.assertEqual(len(names), 2)
        self.assertEqual(names, ['bonobo', 'monkey'])

        res = catalog.searchResults(simiantype='punyhuman', name='anthony')
        self.assertEqual(len(res), 1)
        ob = iter(res).next()
        self.assertEqual((ob.name, ob.simiantype), ('anthony', 'punyhuman'))

        res = catalog.searchResults(simiantype='ape', name='bobo')
        self.assertEqual(len(res), 0)

        res = catalog.searchResults(simiantype='ape', name='mwumi')
        self.assertEqual(len(res), 0)
        self.assertRaises(KeyError, catalog.searchResults,
                          simiantype='monkey', hat='beret')


class CatalogStub:
    implements(ICatalog)
    def __init__(self):
        self.regs = []
        self.unregs = []

    def index_doc(self, docid, doc):
        self.regs.append((docid, doc))

    def unindex_doc(self, docid):
        self.unregs.append(docid)

class Stub:

    __name__ = None
    __parent__ = None



class TestEventSubscribers(unittest.TestCase):

    def setUp(self):
        self.root = setup.placefulSetUp(True)
        sm = self.root.getSiteManager()
        self.utility = setup.addUtility(sm, '', IIntIds, IntIdsStub())
        self.cat = setup.addUtility(sm, '', ICatalog, CatalogStub())
        setSite(self.root)

    def tearDown(self):
        setup.placefulTearDown()

    def test_indexDocSubscriber(self):
        from zope.app.catalog.catalog import indexDocSubscriber
        from zope.app.container.contained import ObjectAddedEvent
        from zope.app.intid.interfaces import IntIdAddedEvent

        ob = Stub()
        ob2 = Stub()

        id = self.utility.register(ob)
        indexDocSubscriber(IntIdAddedEvent(ob, ObjectAddedEvent(ob2)))

        self.assertEqual(self.cat.regs, [(id, ob)])
        self.assertEqual(self.cat.unregs, [])

    def test_reindexDocSubscriber(self):
        from zope.app.catalog.catalog import reindexDocSubscriber
        from zope.lifecycleevent import ObjectModifiedEvent

        ob = Stub()
        id = self.utility.register(ob)

        reindexDocSubscriber(ObjectModifiedEvent(ob))

        self.assertEqual(self.cat.regs, [(1, ob)])
        self.assertEqual(self.cat.unregs, [])

        ob2 = Stub()
        reindexDocSubscriber(ObjectModifiedEvent(ob2))
        self.assertEqual(self.cat.regs, [(1, ob)])
        self.assertEqual(self.cat.unregs, [])


    def test_unindexDocSubscriber(self):
        from zope.app.catalog.catalog import unindexDocSubscriber
        from zope.app.container.contained import ObjectRemovedEvent
        from zope.app.intid.interfaces import IntIdRemovedEvent

        ob = Stub()
        ob2 = Stub()
        ob3 = Stub()
        id = self.utility.register(ob)

        unindexDocSubscriber(
            IntIdRemovedEvent(ob2, ObjectRemovedEvent(ob3)))
        self.assertEqual(self.cat.unregs, [])
        self.assertEqual(self.cat.regs, [])

        unindexDocSubscriber(
            IntIdRemovedEvent(ob, ObjectRemovedEvent(ob3)))
        self.assertEqual(self.cat.unregs, [id])
        self.assertEqual(self.cat.regs, [])


class TestIndexUpdating(unittest.TestCase) :
    """Issue #466: When reindexing a catalog it takes all objects from
    the nearest IntId utility. This is a problem when IntId utility
    lives in another site than the one.

    To solve this issue we simply check whether the objects are living
    within the nearest site.
    """

    def setUp(self):

        setup.placefulSetUp(True)

        from zope.app.catalog.catalog import Catalog
        from zope.app.container.contained import ContainerSublocations

        self.root = setup.buildSampleFolderTree()

        subfolder = self.root[u'folder1'][u'folder1_1']
        root_sm = self.root_sm = setup.createSiteManager(self.root)
        local_sm = self.local_sm = setup.createSiteManager(subfolder)
        self.utility = setup.addUtility(root_sm, '', IIntIds, IntIdsStub())
        self.cat = setup.addUtility(local_sm, '', ICatalog, Catalog())
        self.cat['name'] = StubIndex('__name__', None)

        for obj in self.iterAll(self.root) :
            self.utility.register(obj)

    def tearDown(self):
        setup.placefulTearDown()

    def iterAll(self, container) :
        from zope.app.container.interfaces import IContainer
        for value in container.values() :
            yield value
            if IContainer.providedBy(value) :
                for obj in self.iterAll(value) :
                    yield obj

    def test_visitSublocations(self) :
        """ Test the iterContained method which should return only the
        sublocations which are registered by the IntIds.
        """

        names = sorted([ob.__name__ for i, ob in self.cat._visitSublocations()])
        self.assertEqual(names, [u'folder1_1', u'folder1_1_1', u'folder1_1_2'])

    def test_updateIndex(self):
        """ Setup a catalog deeper within the containment hierarchy
        and call the updateIndexes method. The indexed objects should should
        be restricted to the sublocations.
        """

        self.cat.updateIndexes()
        index = self.cat['name']
        names = sorted([ob.__name__ for i, ob in index.doc.items()])
        self.assertEqual(names, [u'folder1_1', u'folder1_1_1', u'folder1_1_2'])

    def test_optimizedUpdateIndex(self):
        """ Setup a catalog deeper within the containment hierarchy together
        with its intid utility. The catalog will not visit sublocations
        because the intid utility can not contain objects outside the site
        where it is registered.
        """
        utility = setup.addUtility(self.local_sm, '', IIntIds, IntIdsStub())
        subfolder = self.root[u'folder1'][u'folder1_1']
        for obj in self.iterAll(subfolder) :
            utility.register(obj)

        self.cat.updateIndexes()
        index = self.cat['name']
        names = sorted([ob.__name__ for i, ob in index.doc.items()])
        self.assertEqual(names, [u'folder1_1_1', u'folder1_1_2'])


class TestCatalogBugs(placelesssetup.PlacelessSetup, unittest.TestCase):
    """I found that z.a.catalog, AttributeIndex failed to remove the previous
    value/object from the index IF the NEW value is None.
    """

    def test_updateIndexWithNone(self):
        uidutil = IntIdsStub()
        ztapi.provideUtility(IIntIds, uidutil)

        catalog = Catalog()
        index = FieldIndex('author', None)
        catalog['author'] = index

        ob1 = stoopid(author = "joe")
        ob1id = uidutil.register(ob1)
        catalog.index_doc(ob1id, ob1)

        res = catalog.searchResults(author=('joe','joe'))
        names = [x.author for x in res]
        names.sort()
        self.assertEqual(len(names), 1)
        self.assertEqual(names, ['joe'])

        ob1.author = None
        catalog.index_doc(ob1id, ob1)

        #the index must be empty now because None values are never indexed
        res = catalog.searchResults(author=(None, None))
        self.assertEqual(len(res), 0)

    def test_updateIndexFromCallableWithNone(self):
        uidutil = IntIdsStub()
        ztapi.provideUtility(IIntIds, uidutil)

        catalog = Catalog()
        index = FieldIndex('getAuthor', None, field_callable=True)
        catalog['author'] = index

        ob1 = stoopidCallable(author = "joe")

        ob1id = uidutil.register(ob1)
        catalog.index_doc(ob1id, ob1)

        res = catalog.searchResults(author=('joe','joe'))
        names = [x.author for x in res]
        names.sort()
        self.assertEqual(len(names), 1)
        self.assertEqual(names, ['joe'])

        ob1.author = None
        catalog.index_doc(ob1id, ob1)

        #the index must be empty now because None values are never indexed
        res = catalog.searchResults(author=(None, None))
        self.assertEqual(len(res), 0)

class stoopidCallable(object):
    def __init__(self, **kw):
        #leave the door open to not to set self.author
        self.__dict__.update(kw)

    def getAuthor(self):
        return self.author

class TestIndexRaisingValueGetter(placelesssetup.PlacelessSetup, unittest.TestCase):
    """ """
    def test_IndexRaisingValueGetter(self):
        """We can have indexes whose values are determined by callable
        methods.
        Raising an exception in the method should not be silently ignored
        That would cause index corruption -- the index would be out of sync"""
        uidutil = IntIdsStub()
        ztapi.provideUtility(IIntIds, uidutil)

        catalog = Catalog()
        index = FieldIndex('getAuthor', None, field_callable=True)
        catalog['author'] = index

        ob1 = stoopidCallable(author = "joe")
        ob1id = uidutil.register(ob1)
        catalog.index_doc(ob1id, ob1)

        res = catalog.searchResults(author=('joe','joe'))
        names = [x.author for x in res]
        names.sort()
        self.assertEqual(len(names), 1)
        self.assertEqual(names, ['joe'])

        ob2 = stoopidCallable() # no author here, will raise AttributeError
        ob2id = uidutil.register(ob2)
        try:
            catalog.index_doc(ob2id, ob2)
            self.fail("AttributeError exception should be raised")
        except AttributeError:
            #this is OK, we WANT to have the exception
            pass


def test_suite():
    from zope.testing import doctest
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(Test))
    suite.addTest(unittest.makeSuite(TestEventSubscribers))
    suite.addTest(unittest.makeSuite(TestIndexUpdating))
    suite.addTest(unittest.makeSuite(TestCatalogBugs))
    suite.addTest(unittest.makeSuite(TestIndexRaisingValueGetter))
    suite.addTest(doctest.DocTestSuite('zope.app.catalog.attribute'))
    suite.addTest(doctest.DocFileSuite(
        'README.txt',
        setUp=placelesssetup.setUp,
        tearDown=placelesssetup.tearDown,
        ))
    return suite


if __name__ == "__main__":
    unittest.main()
