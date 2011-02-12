from AccessControl import getSecurityManager

from Products.Archetypes import atapi
from Products.Archetypes.public import *
from Products.ATContentTypes.content.base import *
from Products.ArchAddOn.Fields import *
from Products.ArchAddOn.Widgets import *

from Products.PloneServicesCenter.validators import IndustriesValidator
from Products.PloneServicesCenter.content import country

servicesSchema = BaseSchema + Schema ((

    StringField('description',
        accessor='Description',
        # edit_accessor='getDescription',
        #        default_content_type='text/html',
        #        allowable_content_types=('text/html',),

        widget=TextAreaWidget(
            label='Description',
            label_msgid="label_psc_description",
            description='',
            description_msgid="help_psc_description",
            i18n_domain='ploneservicescenter',
            ),
        required=1,
        searchable=1,
        ),
    StringField('country',
        vocabulary=country.vocab,
        validateVocabulary=True,
        countries=country.countries,
        widget=SelectionWidget(
            label='Country',
            label_msgid="label_psc_country_cat",
            description='Select a country',
            description_msgid="help_services_country",
            i18n_domain='ploneservicescenter',
            macro_edit="country_widget"),
        required=0,
        index=('KeywordIndex:schema',),
        ),
    LinesField('industry',               
        validators=IndustriesValidator('validateIndustries'),
        widget=MultiSelectionWidget(
            label="Industry",
            label_msgid="label_psc_industry_cat",
            description="Select a industry from the below list.",
            description_msgid="help_services_industry",
            i18n_domain='ploneservicescenter',
            ),
        required=0,
        vocabulary='getIndustryVocabulary',
        index=('KeywordIndex:schema',),
        ),
    LinkField('url',
        widget=LinkWidget(
            label="URL",
            label_msgid="label_services_url",
            description="Enter the web address (URL). You can copy & paste this from a browser window.",
            description_msgid="help_services_url",
            i18n_domain='ploneservicescenter',
                ),
        required=1,
        ),
    IntegerField('rating',
        widget=SelectionWidget(
            format='select',
            label="Rating",
            label_msgid="label_services_rating",
            description="Select a value of options from the below list by rating.",
            description_msgid="help_services_rating",
            i18n_domain='ploneservicescenter',),
        required=1,
        default=2,
        vocabulary=atapi.IntDisplayList([(i, i) for i in range(1, 4)]),
        write_permission='Manage portal',
        index=('FieldIndex:schema',),        
        ),

    StringField('contactName',
        widget=StringWidget(
            label="Contact Name",
            label_msgid="label_services_contactname",
            description="Enter the contact name.",
            description_msgid="help_services_contactname",
            i18n_domain='ploneservicescenter',
            ),
        required=0,
        searchable=1,
        index=('KeywordIndex:schema',),
        ),

    EmailField('contactEmail',
        widget=EmailWidget(
            label="Email",
            label_msgid="label_services_email",
            description="Enter the email for contacts.",
            description_msgid="help_services_email",
            i18n_domain='ploneservicescenter',
            ),
        required=0,
        searchable=1,
        index=('KeywordIndex:schema',),
        ),

    ComputedField('sortExpression',
        expression='str(context.getRating()) + " " + str(context.Title()).lower()',
        mode='r',
        index=('FieldIndex',),
        widget=StringWidget(
            label='Sort Expression',
            visible={'edit':'invisible','view':'invisible'},
            ),
        ),
        
        

    ))


class BaseServicesContent(ATCTContent):

    _getPossibleRatings = lambda x: range(1, 4)

    global_allow=0
    _at_rename_after_creation = True

    allow_discussion = True

##     def getDescription(self):
##         """
##         Get the raw description
##         """
##         return self.schema["description"].get(self)

##     def Description(self):
##         """
##         Get the formatted description
##         """
##         return newline_to_br(self.getDescription())

    def canSeeProvider(self):
        """
        Check if we are allowed to see the provider of the site
        """
        provider = self.getProvider()
        if not provider:
            return False
        user = getSecurityManager().getUser()
        return user.has_permission("View", provider)

    def getProvidersReferences(self):
        """
        Return a sorted list of references
        """
        field = self.getWrappedField('provider')
        providers = list(field._Vocabulary(self).items())
        providers.sort(lambda a,b: cmp(a[1].lower(), b[1].lower()))
        return DisplayList(providers)

    def getCountry(self, **kw):
        # lowercase to tolerate uppercase values from plone.net
        value = self.getField('country').get(self, **kw)
        if isinstance(value, (str, unicode)):
            return value.lower()
        return value
