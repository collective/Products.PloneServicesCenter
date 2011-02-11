from Products.Archetypes.public import *
from Services import *
from zope.interface import implements
from Products.PloneServicesCenter.interfaces import ICaseStudy

schema = servicesSchema + Schema ((

    TextField('body',
        allowable_content_types=('text/html',),
        default_content_type='text/html',
        default_output_type='text/html',
        widget=RichWidget(
            label="Detailed information",
            label_msgid="label_psc_detailed_info",
            description="Enter the details description about this case study.",
            description_msgid="help_casestudy_body",
            i18n_domain='ploneservicescenter',
            ),
        required=0,
	searchable=1,
        ),

    ImageField('screenshot',
        original_size=(800,600),
        sizes={
        'preview': (400, 400),
        'view'   : (250, 250),
        'mini'   : (200, 200),
        'thumb'  : (128, 128),
        'tile'   : (64, 64),
        'icon'   : (32, 32),
        'listing': (16, 16),
        },
        widget=ImageWidget(
            label="Screenshot",
            label_msgid="label_psc_screenshot",
            description="Add a screenshot for the case study. Max 150x75 pixels (will be resized if bigger).",
            description_msgid="help_casestudy_screenshot",
            i18n_domain='ploneservicescenter',
        ),
        ),
    ImageField('logo',
        max_size=(150, 75),
        widget=ImageWidget(
            label="Logo",
            label_msgid="label_psc_logo",
            description="Add a logo for the case study (normally the customer logo). Max 150x75 pixels (will be resized if bigger).",
            description_msgid="help_casestudy_logo",
            i18n_domain='ploneservicescenter',
        ),
        ),

    ReferenceField('provider',
        relationship='providerToCaseStudy',
        allowed_types=('Provider',),
        vocabulary_display_path_bound=-1,
        vocabulary="getProvidersReferences",
        widget=ReferenceWidget(
            label="Provider",
            label_msgid="label_psc_provider_cat",
            description="Select a provider from the below listing for the case study.",
            description_msgid="help_casestudy_provider",
            i18n_domain='ploneservicescenter',
        ),
        ),

    ))


class CaseStudy(BaseServicesContent):
    """Shows off a Plone site or project built for a customer."""

    implements(ICaseStudy)
    schema = schema
    archetype_name = "Case study"
    typeDescription= "Shows off a Plone site or project built for a customer."
    typeDescMsgId  = "help_casestudy_archetype"

registerType(CaseStudy, 'PloneServicesCenter')

