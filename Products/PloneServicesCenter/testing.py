# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class ServicesFixture(PloneSandboxLayer):

    """
    This layer is the Test class base.

    Check out all tests on this package:

    ./bin/test -s Products.PloneServicesCenter --list-tests
    """

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.ArchAddOn
        self.loadZCML(package=Products.ArchAddOn)
        import Products.PloneServicesCenter
        self.loadZCML(package=Products.PloneServicesCenter)

        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'Products.ArchAddOn')
        z2.installProduct(app, 'Products.PloneServicesCenter')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        getToolByName(portal, 'portal_quickinstaller').installProduct(
            'Products.ArchAddOn')
        self.applyProfile(portal, 'Products.PloneServicesCenter:default')

        # z2.login(aq_parent(portal).acl_users, 'admin')

        # set the default workflow
        # wftool = getToolByName(portal, 'portal_workflow')
        workflow_tool = portal['portal_workflow']
        workflow_tool.setDefaultChain('simple_publication_workflow')
        # Publish the folders
        for id_ in ('case-studies', 'sites', 'providers'):
            # wftool.doActionFor(portal.support[id_], 'publish')
            workflow_tool.doActionFor(portal.support[id_], 'publish')
        # z2.logout()

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.ArchAddOn')
        z2.uninstallProduct(app, 'Products.PloneServicesCenter')

SERVICES_FIXTURE = ServicesFixture()

"""
We use this base for all the tests in this package. If necessary,
we can put common utility or setup code in here. This applies to unit
test cases.
"""
INTEGRATION_TESTING = IntegrationTesting(
    bases=(SERVICES_FIXTURE,),
    name='Services:Integration'
)

"""
We use this for functional integration tests. Again, we can put basic
common utility or setup code in here.
"""
SERVICES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SERVICES_FIXTURE,),
    name='Services:Functional'
)

"""
We use this for functional integration tests with robot framework. Again,
we can put basic common utility or setup code in here.
"""
ROBOT_TESTING = FunctionalTesting(
    bases=(SERVICES_FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='Services:Robot',
)
