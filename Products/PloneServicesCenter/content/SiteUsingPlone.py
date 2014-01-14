from AccessControl import getSecurityManager

from zope.interface import implements

from Products.Archetypes import atapi

from Products.PloneServicesCenter import PSCMessageFactory as _
from Products.PloneServicesCenter.interfaces import ISiteUsingPlone
from Products.PloneServicesCenter.content import Services

schema = Services.servicesSchema + atapi.Schema((

    atapi.ReferenceField('provider',
        widget=atapi.ReferenceWidget(
            checkbox_bound=0,
            label=_(u"label_psc_provider_cat", default=u"Provider"),
            description=_(u"help_siteuseplone_provider", default=u"Select provider(s) from the below listing for the Site that Use Plone."),
            i18n_domain='ploneservicescenter',
        ),
        relationship='providerToSiteUsingPlone',
        allowed_types=('Provider',),
        vocabulary_display_path_bound=-1,
        vocabulary="getProvidersReferences",
        multiValued=True,
        ),

    ))


class SiteUsingPlone(Services.BaseServicesContent):
    """Site using Plone.

    Not a full case study, but just a description and URL.
    """
    implements(ISiteUsingPlone)
    schema = schema
    archetype_name = "Site using Plone"
    typeDescription = """\
Site using Plone. Not a full case study, but just a description and URL."""
    typeDescMsgId = "help_siteuseplone_archetype"

    def getProviders(self):
        provider = self.getProvider()
        if not isinstance(provider, list):
            return [provider]
        return provider

    def canSeeProvider(self):
        """
        Check if we are allowed to see the provider of the site
        """
        providers = self.getProviders()
        if not providers:
            return False
        user = getSecurityManager().getUser()
        return True in [user.has_permission('View', p) for p in providers]

atapi.registerType(SiteUsingPlone, 'PloneServicesCenter')
