from ServicesFolder import *
from zope.interface import implements
from Products.PloneServicesCenter.interfaces import ISiteUsingPloneFolder

class SiteUsingPloneFolder(BaseServicesFolder):
    """Folder for sites using Plone."""
    
    implements(ISiteUsingPloneFolder)
    allowed_content_types=['SiteUsingPlone']

    actions = (
        {
            'id'          : 'view',
            'name'        : 'View',
            'action'      : 'string:${object_url}/sites_listing',
            'permissions' : ('View',)
        },
    )
    

registerType(SiteUsingPloneFolder, 'PloneServicesCenter')
