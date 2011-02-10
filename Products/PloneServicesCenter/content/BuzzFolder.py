from ServicesFolder import *
from zope.interface import implements
from Products.PloneServicesCenter.interfaces import IBuzzFolder

class BuzzFolder(BaseServicesFolder):
    """Folder for Plone buzz items."""

    implements(IBuzzFolder)
    allowed_content_types=['Buzz']


    actions = (
        {
            'id'          : 'view',
            'name'        : 'View',
            'action'      : 'string:${object_url}/buzz_listing',
            'permissions' : ('View',)
        },
    )
    

registerType(BuzzFolder)
