from ServicesFolder import *
from zope.interface import implements
from Products.PloneServicesCenter.interfaces import IProviderFolder

class ProviderFolder(BaseServicesFolder):
    """Folder for providers."""
    
    implements(IProviderFolder)
    allowed_content_types=['Provider']

    actions = (
        {
            'id'          : 'view',
            'name'        : 'View',
            'action'      : 'string:${object_url}/by-country',
            'permissions' : ('View',)
        },
	)

registerType(ProviderFolder)
