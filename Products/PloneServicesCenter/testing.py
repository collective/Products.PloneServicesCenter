from plone.testing import z2
from plone.app import testing

from Products.CMFCore.utils import getToolByName


class ServicesFixture(testing.PloneSandboxLayer):
    default_bases = (testing.PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneServicesCenter
        self.loadZCML(package=Products.PloneServicesCenter)

        # Install product and call its initialize() function
        z2.installProduct(app, 'Products.ArchAddOn')
        z2.installProduct(app, 'Products.PloneServicesCenter')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        getToolByName(portal, 'portal_quickinstaller').installProduct(
            'Products.ArchAddOn')
        self.applyProfile(portal, 'Products.PloneServicesCenter:default')

SERVICES_FIXTURE = ServicesFixture()
SERVICES_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(SERVICES_FIXTURE,), name="Services:Functional")
