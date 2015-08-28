# -*- coding: utf-8 -*-

from Products.Archetypes import atapi

from Products.PloneServicesCenter.content import ServicesFolder
from Products.PloneServicesCenter.interfaces import IBuzzFolder

from zope.interface import implements


class BuzzFolder(ServicesFolder.BaseServicesFolder):
    """Folder for Plone buzz items."""

    implements(IBuzzFolder)
    allowed_content_types = ['Buzz']

    actions = (
        {
            'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/buzz_listing',
            'permissions': ('View',)
        },
    )


atapi.registerType(BuzzFolder, 'PloneServicesCenter')
