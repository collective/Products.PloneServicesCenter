from Products.Archetypes.public import *
from Services import *
from zope.interface import implements
from Products.PloneServicesCenter.interfaces import ISiteUsingPlone

schema = servicesSchema + Schema ((

    ImageField('screenshot',
               widget=ImageWidget(
                   label="Screenshot",
                   label_msgid="label_psc_screenshot",
                   description="Add a screenshot for the Site that Use Plone. Max 150x75 pixels (will be resized if bigger).",
                   description_msgid="help_siteuseplone_screenshot",
                   i18n_domain='ploneservicescenter',
               ),
               sizes= {'large'   : (768, 768),
                       'preview' : (400, 400),
                       'view'    : (250, 250),
                       'mini'    : (200, 200),
                       'thumb'   : (128, 128),
                       'tile'    :  (64, 64),
                       'icon'    :  (32, 32),
                       'listing' :  (16, 16),
                      },
               required=1,
        ),

    ReferenceField('provider',
        widget=ReferenceWidget(
            checkbox_bound=0,
            label="Provider",
            label_msgid="label_psc_provider_cat",
            description="Select a provider from the below listing for the Site that Use Plone.",
            description_msgid="help_siteuseplone_provider",
            i18n_domain='ploneservicescenter',),
        relationship='providerToSiteUsingPlone',
        allowed_types=('Provider',),
        vocabulary_display_path_bound=-1,
        vocabulary="getProvidersReferences",
        ),

    ))

# schema["url"].required = False
# schema["url"].widget.description = "Leave empty if it is an intranet site."

class SiteUsingPlone(BaseServicesContent):
    """Site using Plone.

    Not a full case study, but just a description and URL.
    """
    implements(ISiteUsingPlone)
    schema = schema
    archetype_name = "Site using Plone"
    typeDescription= "Site using Plone. Not a full case study, but just a description and URL."
    typeDescMsgId  = "help_siteuseplone_archetype"

registerType(SiteUsingPlone, 'PloneServicesCenter')

