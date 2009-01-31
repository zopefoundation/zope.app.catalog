##############################################################################
#
# Copyright (c) 2001, 2002 Zope Corporation and Contributors.
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
"""Component architecture related 'zope' ZCML namespace directive interfaces

$Id$
"""
__docformat__ = 'restructuredtext'

import zope.configuration.fields
import zope.security.zcml
import zope.interface
import zope.schema
from zope.component.zcml import IBasicComponentInformation

from zope.app.component.i18n import ZopeMessageFactory as _

class IDefaultViewName(zope.interface.Interface):
    """A string that contains the default view name

    A default view name is used to select a view when a user hasn't
    specified one.
    """

class IBasicViewInformation(zope.interface.Interface):
    """This is the basic information for all views."""

    for_ = zope.configuration.fields.Tokens(
        title=_("Specifications of the objects to be viewed"),
        description=_("""This should be a list of interfaces or classes
        """),
        required=True,
        value_type=zope.configuration.fields.GlobalObject(
          missing_value=object(),
          ),
        )

    permission = zope.security.zcml.Permission(
        title=_("Permission"),
        description=_("The permission needed to use the view."),
        required=False,
        )

    class_ = zope.configuration.fields.GlobalObject(
        title=_("Class"),
        description=_("A class that provides attributes used by the view."),
        required=False,
        )

    layer = zope.configuration.fields.GlobalInterface(
        title=_("The layer the view is in."),
        description=_("""
        A skin is composed of layers. It is common to put skin
        specific views in a layer named after the skin. If the 'layer'
        attribute is not supplied, it defaults to 'default'."""),
        required=False,
        )

    allowed_interface = zope.configuration.fields.Tokens(
        title=_("Interface that is also allowed if user has permission."),
        description=_("""
        By default, 'permission' only applies to viewing the view and
        any possible sub views. By specifying this attribute, you can
        make the permission also apply to everything described in the
        supplied interface.

        Multiple interfaces can be provided, separated by
        whitespace."""),
        required=False,
        value_type=zope.configuration.fields.GlobalInterface(),
        )

    allowed_attributes = zope.configuration.fields.Tokens(
        title=_("View attributes that are also allowed if the user"
                " has permission."),
        description=_("""
        By default, 'permission' only applies to viewing the view and
        any possible sub views. By specifying 'allowed_attributes',
        you can make the permission also apply to the extra attributes
        on the view object."""),
        required=False,
        value_type=zope.configuration.fields.PythonIdentifier(),
        )

class IBasicResourceInformation(zope.interface.Interface):
    """
    Basic information for resources
    """

    name = zope.schema.TextLine(
        title=_("The name of the resource."),
        description=_("The name shows up in URLs/paths. For example 'foo'."),
        required=True,
        default=u'',
        )

    provides = zope.configuration.fields.GlobalInterface(
        title=_("The interface this component provides."),
        description=_("""
        A view can provide an interface.  This would be used for
        views that support other views."""),
        required=False,
        default=zope.interface.Interface,
        )

    type = zope.configuration.fields.GlobalInterface(
        title=_("Request type"),
        required=True
        )


class IViewDirective(IBasicViewInformation, IBasicResourceInformation):
    """Register a view for a component"""

    factory = zope.configuration.fields.Tokens(
        title=_("Factory"),
        required=False,
        value_type=zope.configuration.fields.GlobalObject(),
        )

############################################################################
# BBB: Deprecated; use browser:defaultView instead. Will go away in 3.3.
class IDefaultViewDirective(IBasicResourceInformation):
    """
    *BBB: DEPRECATED*

    Use ``browser:defaultView`` instead.

    The name of the view that should be the default.

    This name refers to view that should be the
    view used by default (if no view name is supplied
    explicitly).
    """

    for_ = zope.configuration.fields.GlobalInterface(
        title=_("The interface this view is the default for."),
        description=_("""
        Specifies the interface for which the default view is declared. All
        objects implementing this interface make use of this default
        setting. If this attribute is not specified, the default is available
        for all objects."""),
        required=False,
        )
############################################################################


class IResourceDirective(IBasicComponentInformation,
                         IBasicResourceInformation):
    """Register a resource"""

    layer = zope.configuration.fields.GlobalInterface(
        title=_("The layer the resource is in."),
        required=False,
        )

    allowed_interface = zope.configuration.fields.Tokens(
        title=_("Interface that is also allowed if user has permission."),
        required=False,
        value_type=zope.configuration.fields.GlobalInterface(),
        )

    allowed_attributes = zope.configuration.fields.Tokens(
        title=_("View attributes that are also allowed if user"
                " has permission."),
        required=False,
        value_type=zope.configuration.fields.PythonIdentifier(),
        )
