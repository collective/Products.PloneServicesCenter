# -*- coding: utf-8 -*-

from Products.Archetypes import atapi

from Products.PloneServicesCenter.content import ServicesFolder
from Products.PloneServicesCenter.interfaces import ISiteUsingPloneFolder

from zope.interface import implements


class SiteUsingPloneFolder(ServicesFolder.BaseServicesFolder):
    """Folder for sites using Plone."""

    implements(ISiteUsingPloneFolder)
    allowed_content_types = ['SiteUsingPlone']

    actions = (
        {
            'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/sites_listing',
            'permissions': ('View',)
        },
    )


atapi.registerType(SiteUsingPloneFolder, 'PloneServicesCenter')
