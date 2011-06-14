from zope.interface import implements

from Products.Archetypes import atapi

from Products.PloneServicesCenter import PSCMessageFactory as _
from Products.PloneServicesCenter.interfaces import IBuzz
from Products.PloneServicesCenter.content import Services


schema = Services.servicesSchema + atapi.Schema((

    atapi.TextField('body',
        widget=atapi.RichWidget(
            label=_(u"label_psc_detailed_info", default=u"Detailed information"),
            description=_(u"help_buzz_body", default=u"Enter the details description about this buzz."),
            i18n_domain='ploneservicescenter',
        ),
        allowable_content_types=('text/html',),
        default_content_type='text/html',
        default_output_type='text/html',
        required=0,
        searchable=1,
    ),

    atapi.ImageField('logo',
        widget=atapi.ImageWidget(
            label=_(u"label_general_logo", default=u"Logo"),
            description=_(u"help_buzz_logo", default=u"Add a logo for the case study (normally the customer logo). Max 150x75 pixels (will be resized if bigger)."),
            i18n_domain='ploneservicescenter',
        ),
        sizes={'large': (768, 768),
               'preview': (400, 400),
               'view': (250, 250),
               'mini': (200, 200),
               'thumb': (128, 128),
               'tile': (64, 64),
               'icon': (32, 32),
               'listing': (16, 16),
              },
    ),

    atapi.ReferenceField('provider',
        widget=atapi.ReferenceWidget(
            label=_(u"label_psc_provider_cat", default=u"Provider"),
            description=_(u"help_buzz_provider", default=u"Select a provider from the below listing for the media coverage."),
            checkbox_bound=0,
            i18n_domain='ploneservicescenter',
        ),
        relationship='providerToBuzz',
        allowed_types=('Provider',),
        vocabulary_display_path_bound=-1,
        vocabulary="getProvidersReferences",
    ),

))

class Buzz(Services.BaseServicesContent):
    """A link to media coverage of Plone."""

    implements(IBuzz)
    schema = schema
    archetype_name = "Media Coverage"
    typeDescription = "A link to media coverage of Plone."
    typeDescMsgId = "help_buzz_archetype"

atapi.registerType(Buzz, 'PloneServicesCenter')
