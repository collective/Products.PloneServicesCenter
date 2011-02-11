from ServicesFolder import *
from zope.interface import implements
from Products.PloneServicesCenter.interfaces import ICaseStudyFolder

class CaseStudyFolder(BaseServicesFolder):
    """Folder for case studies."""

    implements(ICaseStudyFolder)
    allowed_content_types=['CaseStudy']
    

    actions = (
        {
            'id'          : 'view',
            'name'        : 'View',
            'action'      : 'string:${object_url}/casestudy_listing',
            'permissions' : ('View',)
        },
    )

registerType(CaseStudyFolder, 'PloneServicesCenter')
