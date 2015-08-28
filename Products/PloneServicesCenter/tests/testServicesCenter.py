# -*- coding: utf-8 -*-

""" PloneServicesCenterTestCase """

from Products.PloneServicesCenter.config import CREATE_INITIAL_CONTENT
from Products.PloneServicesCenter.tests import PloneServicesCenterTestCase as PSCTestCase

import os
import sys

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))


class TestInstallation(PSCTestCase.PloneServicesCenterTestCase):

    def afterSetUp(self):
        pass

    def testPortalTypes(self):
        types = self.portal.portal_types.objectIds()
        self.assertTrue('Buzz' in types)
        self.assertTrue('BuzzFolder' in types)
        self.assertTrue('CaseStudy' in types)
        self.assertTrue('CaseStudyFolder' in types)
        self.assertTrue('Provider' in types)
        self.assertTrue('ProviderFolder' in types)
        self.assertTrue('SiteUsingPlone' in types)
        self.assertTrue('SiteUsingPloneFolder' in types)

    def testAddingBuzzFolder(self):
        self.folder.invokeFactory('BuzzFolder', 'buzz')
        items = self.folder.objectIds()
        self.assertTrue('buzz' in items)

    def testAddingCaseStudyFolder(self):
        self.folder.invokeFactory('CaseStudyFolder', 'case_studies')
        items = self.folder.objectIds()
        self.assertTrue('case_studies' in items)

    def testAddingProviderFolder(self):
        self.folder.invokeFactory('ProviderFolder', 'providers')
        items = self.folder.objectIds()
        self.assertTrue('providers' in items)

    def testAddingSiteUsingPloneFolder(self):
        self.folder.invokeFactory('SiteUsingPloneFolder', 'plone_sites')
        items = self.folder.objectIds()
        self.assertTrue('plone_sites' in items)


class TestAddingStuff(PSCTestCase.PloneServicesCenterTestCase):

    def afterSetUp(self):
        self.folder.invokeFactory('BuzzFolder', 'buzz')
        self.folder.invokeFactory('CaseStudyFolder', 'case_studies')
        self.folder.invokeFactory('ProviderFolder', 'providers')
        self.folder.invokeFactory('SiteUsingPloneFolder', 'plone_sites')
        self.buzz = self.folder.buzz
        self.case_studies = self.folder.case_studies
        self.providers = self.folder.providers
        self.plone_sites = self.folder.plone_sites

    def testAddingProviders(self):
        self.providers.invokeFactory('Provider', 'provider1')
        self.assertTrue('provider1' in self.providers.objectIds())
        self.assertTrue(self.providers.getProviders())

    def testAddingBuzz(self):
        self.buzz.invokeFactory('Buzz', 'buzz1')
        self.assertTrue('buzz1' in self.buzz.objectIds())

    def testAddingCaseStudies(self):
        self.case_studies.invokeFactory('CaseStudy', 'cs1')
        self.assertTrue('cs1' in self.case_studies.objectIds())
        self.assertTrue(self.case_studies.getCaseStudies())

    def testAddingSites(self):
        self.plone_sites.invokeFactory('SiteUsingPlone', 'site1')
        self.assertTrue('site1' in self.plone_sites.objectIds())
        self.assertTrue(self.plone_sites.getSitesUsingPlone())


class TestInstallingDefaultContent(PSCTestCase.PloneServicesCenterTestCase):

    def afterSetUp(self):
        pass

    def testProvidersAdded(self):
        # a crude test that there is content in the providers folder
        if CREATE_INITIAL_CONTENT is True:
            items = self.portal.objectIds()
            self.assertTrue('providers' in items)
        else:
            pass

    def testBuzzAdded(self):
        if CREATE_INITIAL_CONTENT is True:
            items = self.portal.objectIds()
            self.assertTrue('buzz' in items)
        else:
            pass

    def testCaseStudiesAdded(self):
        if CREATE_INITIAL_CONTENT is True:
            items = self.portal.objectIds()
            self.assertTrue('case-studies' in items)
        else:
            pass

    def testSitesAdded(self):
        if CREATE_INITIAL_CONTENT is True:
            items = self.portal.objectIds()
            self.assertTrue('sites' in items)
        else:
            pass


class TestWorkflow(PSCTestCase.PloneServicesCenterTestCase):

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow

        self.portal.acl_users._doAddUser('member', 'secret', ['Member'], [])
        self.portal.acl_users._doAddUser(
            'reviewer', 'secret', ['Reviewer'], [])
        self.portal.acl_users._doAddUser('manager', 'secret', ['Manager'], [])

        self.folder.invokeFactory('SiteUsingPloneFolder', 'plone_sites')
        self.plone_sites = self.folder.plone_sites

    def testMemberAddsSite(self):

        self.login()
        self.plone_sites.invokeFactory('SiteUsingPlone', 'site1')
        self.assertTrue('site1' in self.plone_sites.objectIds())


def test_suite():
    from unittest import makeSuite
    from unittest import TestSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestAddingStuff))
    suite.addTest(makeSuite(TestInstallingDefaultContent))
    suite.addTest(makeSuite(TestWorkflow))
    return suite
