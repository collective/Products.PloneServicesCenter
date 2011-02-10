# -*- coding: utf-8 -*-

# This file contains some migration methods

from Products.CMFCore.utils import getToolByName

def migrateCountries(self):
    """
    Migrate countries in plone.net content types
    """
    pc = getToolByName(self, "portal_catalog")
    brains = pc(portal_type=("Buzz", "CaseStudy", "Provider", "SiteUsingPlone"))
    total = 0
    migrated = 0
    for brain in brains:
        total += 1
        countries = brain.getCountry
        if isinstance(countries, (list, tuple)):
            obj = brain.getObject()
            country = countries and countries[0] or None
            obj.setCountry(country)
            obj.reindexObject()
            migrated += 1

    return "%d objects found, %d migrated" % (total, migrated)
