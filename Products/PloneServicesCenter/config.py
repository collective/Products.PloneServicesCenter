# -*- coding: utf-8 -*-

from Globals import package_home
from Products.CMFCore.permissions import AddPortalContent

ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'PloneServicesCenter'
SKINS_DIR = 'skins'

GLOBALS = globals()

PACKAGE_HOME = package_home(GLOBALS)
# yeah, a list - since we modify this globally from the testcase...


CREATE_INITIAL_CONTENT = False
