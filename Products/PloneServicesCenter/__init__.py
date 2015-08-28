# -*- coding: utf-8 -*-

from Products.Archetypes.public import listTypes
from Products.Archetypes.public import process_types
from Products.CMFCore import utils as CMFCoreUtils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.PloneServicesCenter.config import ADD_CONTENT_PERMISSION
from Products.PloneServicesCenter.config import GLOBALS
from Products.PloneServicesCenter.config import PROJECTNAME
from Products.PloneServicesCenter.config import SKINS_DIR
from Products.PloneServicesCenter.validators import IndustriesValidator
from Products.validation import validation
from zope.i18nmessageid import MessageFactory

PSCMessageFactory = MessageFactory('ploneservicescenter')

registerDirectory(SKINS_DIR, GLOBALS)

validation.register(IndustriesValidator('validateIndustries'))


def initialize(context):

    # Get all the content types in the content directory
    from Products.PloneServicesCenter import content
    content  # pyflakes

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    CMFCoreUtils.ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
