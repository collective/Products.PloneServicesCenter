## -*- coding: utf-8 -*-

from Products.CMFCore.permissions import setDefaultRoles

default_roles = { 'Reply to item' : ('Manager', 'Reviewer'),
                  'Show item replies' : ('Manager', 'Reviewer', 'Owner'), }

def setPortalDefaultPermissions(portal):
    for perm, roles in default_roles.items():
        setDefaultRoles(perm, roles)
        portal.manage_permission(perm, roles)
        perms = portal.permission_settings(perm)
        if not perms:
            portal.__ac_permission__ += ( (perm, ()), )
