# -*- coding: utf-8 -*-

from Products.Archetypes import atapi

from Products.PloneServicesCenter.content import ServicesFolder
from Products.PloneServicesCenter.interfaces import IProviderFolder

from zope.interface import implements


class ProviderFolder(ServicesFolder.BaseServicesFolder):
    """Folder for providers."""

    implements(IProviderFolder)
    allowed_content_types = ['Provider']

    actions = (
        {
            'id': 'view',
            'name': 'View',
            'action': 'string:${object_url}/by-country',
            'permissions': ('View',)
        },
    )

atapi.registerType(ProviderFolder, 'PloneServicesCenter')
