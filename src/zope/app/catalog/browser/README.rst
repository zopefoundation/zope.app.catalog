Catalogs
========

Catalogs are simple tools used to supppot searching.  A catalog
manages a collection of indexes, and aranges for objects to indexed
with it's contained indexes.

TODO: Filters
      Catalogs should provide the option to filter the objects the
      catalog. This would facilitate the use of separate catalogs for
      separate purposes.  It should be possible to specify a a
      collection of types (interfaces) to be cataloged and a filtering
      expression.  Perhaps another option would be to be the ability
      to specify a names filter adapter.

Catalogs use a unique-id tool to assign short (integer) ids to
objects.  Before creating a catalog, you must create a intid tool:

  >>> print(http(r"""
  ... POST /++etc++site/default/@@+/action.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ... Referer: http://localhost:8081/++etc++site/default/@@+
  ...
  ... type_name=BrowserAdd__zope.intid.IntIds&id=&add=+Add+""",
  ... handle_errors=False))
  HTTP/1.1 303 ...

And register it:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.name', ''),
  ...     ('field.provided', 'zope.intid.interfaces.IIntIds'),
  ...     ('field.provided-empty-marker', '1'),
  ...     ('field.comment', ''),
  ...     ('field.actions.register', 'Register'),
  ...     ])
  >>> print(http(b"""
  ... POST /++etc++site/default/IntIds/addRegistration.html HTTP/1.1
  ... Authorization: Basic mgr:mgrpw
  ... Referer: http://localhost:8081/++etc++site/default/IntIds/
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 303 ...
  ...


Moving short-id management outside of catalogs make it possible to
join searches accross multiple catalogs and indexing tools
(e.g. relationship indexes).

TODO: Filters?
      Maybe unique-id tools should be filtered as well, however, this
      would limit the value of unique id tools for providing
      cross-catalog/cross-index merging.  At least the domain for a
      unique id tool would be broader than the domain of a catalog.
      The value of filtering in the unique id tool is that it limits
      the amount of work that needs to be done by catalogs.
      One obvious aplication is to provide separate domains for
      ordinary and meta content. If we did this, then we'd need to be
      able to select, and, perhaps, alter, the unique-id tool used by
      a catalog.

Once we have a unique-id tool, you can add a catalog:

  >>> print(http(r"""
  ... POST /++etc++site/default/@@+/action.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ... Referer: http://localhost:8081/++etc++site/default/@@+
  ...
  ... type_name=BrowserAdd__zope.catalog.catalog.Catalog&id=&add=+Add+"""))
  HTTP/1.1 303 ...

and register it:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.name', ''),
  ...     ('field.provided', 'zope.catalog.interfaces.ICatalog'),
  ...     ('field.provided-empty-marker', '1'),
  ...     ('field.comment', ''),
  ...     ('field.actions.register', 'Register'),
  ...     ])
  >>> print(http(b"""
  ... POST /++etc++site/default/Catalog/addRegistration.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/++etc++site/default/Catalog/
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 ...


Once we have a catalog, we can add indexes to it.  Before we add an
index, let's add a templated page.  When adding indexes, existing
objects are indexed, so the document we add now will appear in the
index:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.source', '<html>\n<body>\nNow is the time, for all good'
  ...      ' dudes to come to the aid of their country.\n</body>\n</html>'),
  ...     ('field.expand.used', ''),
  ...     ('field.evaluateInlineCode.used', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'dudes'),
  ...     ])
  >>> print(http(b"""
  ... POST /+/zope.app.zptpage.ZPTPage%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost:8081/+/zope.app.zptpage.ZPTPage=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 ...

Perhaps the most common type of index to be added is a text index.
Most indexes require the specification of an interface, an attribute,
and an indication of whether the attribute must be called.

TODO: Simplify the UI for selecting interfaces and attributes
      There are a number of ways the UI for this could be made more
      user friendly:

      - If the user selects an interface, we could then provide a
        select list of possible attributes and we could determine the
        callability.  Perhaps selection of an interface should be
        required.

      - An index should have a way to specify default values. In
        particular, text indexes usially use ISearchableText and
        searchableText.

For text indexes, one generally uses
`zope.index.text.interfaces.ISearchableText`,
`getSearchableText` and True.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.interface', 'zope.index.text.interfaces.ISearchableText'),
  ...     ('field.interface-empty-marker', '1'),
  ...     ('field.field_name', 'getSearchableText'),
  ...     ('field.field_callable.used', ''),
  ...     ('field.field_callable', 'on'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', ''),
  ...     ])
  >>> print(http(b"""
  ... POST /++etc++site/default/Catalog/+/AddTextIndex%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost:8081/++etc++site/default/Catalog/+/AddTextIndex=
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 303 ...


We can visit the advanced tab of the catalog to get some index
statistics.  Doing so, we see that we have a single document and that
the total word count is 8. The word count is only 8 because ssome stop
words have been eliminated.

  >>> print(http(r"""
  ... GET /++etc++site/default/Catalog/@@advanced.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/++etc++site/default/Catalog/@@contents.html
  ... """))
  HTTP/1.1 200 ...
  ...
  <table class="listing" summary="Indexes">
     <tr><th>Index</th>
         <th>Document Count</th>
         <th>Word Count</th>
     </tr>
     <tr>
         <td>TextIndex</td>
         <td>1</td>
         <td>10</td>
      </tr>
  </table>
  ...

We can ask the index to reindex the objects:

  >>> print(http(r"""
  ... POST /++etc++site/default/Catalog/@@reindex.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/++etc++site/default/Catalog/@@contents.html
  ... """))
  HTTP/1.1 303 ...
  ...
  Location: @@advanced.html


Now lets add some more pages:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.source', '<html>\n<body>\nDudes, we really need to switch'
  ...      ' to Zope 3 now.\n</body>\n</html>'),
  ...     ('field.expand.used', ''),
  ...     ('field.evaluateInlineCode.used', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'zope3'),
  ...     ])
  >>> print(http(b"""
  ... POST /+/zope.app.zptpage.ZPTPage%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost:8081/+/zope.app.zptpage.ZPTPage=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.source', '<html>\n<body>\n<p>Writing tests as doctests makes'
  ...      ' them much more understandable.</p>\n'
  ...      '<p>Python 2.4 has major enhancements to the doctest module.</p>\n'
  ...      '</body>\n</html>'),
  ...     ('field.expand.used', ''),
  ...     ('field.evaluateInlineCode.used', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'doctest'),
  ...     ])
  >>> print(http(b"""
  ... POST /+/zope.app.zptpage.ZPTPage%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost:8081/+/zope.app.zptpage.ZPTPage=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 ...

Now, if we visit the catalog advanced tab, we can see that the 3
documents have been indexed and that the word count has increased to 30:

  >>> print(http(r"""
  ... GET /++etc++site/default/Catalog/@@advanced.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Referer: http://localhost:8081/++etc++site/default/Catalog/@@contents.html
  ... """))
  HTTP/1.1 200 ...
  ...
  <table class="listing" summary="Indexes">
     <tr><th>Index</th>
         <th>Document Count</th>
         <th>Word Count</th>
     </tr>
     <tr>
         <td>TextIndex</td>
         <td>3</td>
         <td>33</td>
      </tr>
  </table>
  ...


Now that we have a catalog with some documents indexed, we can search
it.  The catalog is really meant to be used from Python:

  >>> root = getRootFolder()

We'll make our root folder the site (this would normally be done by
the publisher):

  >>> from zope.component.hooks import setSite
  >>> setSite(root)

Now, we'll get the catalog:

  >>> import zope.component
  >>> from zope.catalog.interfaces import ICatalog
  >>> catalog = zope.component.getUtility(ICatalog)

And search it to find the names of all of the documents that contain
the word 'now':

  >>> results = catalog.searchResults(TextIndex='now')
  >>> [result.__name__ for result in results]
  ['dudes', 'zope3']

TODO
   This stuff needs a lot of work.  The indexing interfaces, despite
   being rather elaborate are still a bit too simple.  There really
   should be more provision for combining result.  In particular,
   catalog should have a search interface that returns ranked docids,
   rather than documents.

You don't have to use the search algorithm build into the catalog. You
can implement your own search algorithms and use them with a catalog's
indexes.
