# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager

from Products.ATContentTypes.content import base
from Products.ArchAddOn import public
from Products.Archetypes import atapi

from Products.PloneServicesCenter import PSCMessageFactory as _
from Products.PloneServicesCenter.content import country
from Products.PloneServicesCenter.validators import IndustriesValidator

servicesSchema = atapi.BaseSchema + atapi.Schema((

    atapi.StringField(
        'description',
        accessor='Description',
        widget=atapi.TextAreaWidget(
            label=_(u'label_psc_description', default=u'Description'),
            description=_(u'help_psc_description', default=u''),
            i18n_domain='ploneservicescenter',
        ),
        required=1,
        searchable=1,
    ),

    atapi.StringField(
        'country',
        vocabulary=country.vocab,
        validateVocabulary=True,
        countries=country.countries,
        widget=atapi.SelectionWidget(
            label=_(u'label_psc_country_cat', default=u'Country'),
            description=_(u'help_services_country', default=u'Select a country'),
            i18n_domain='ploneservicescenter',
            macro_edit='country_widget'
        ),
        required=0,
        index=('KeywordIndex:schema',),
    ),

    atapi.LinesField(
        'industry',
        validators=IndustriesValidator('validateIndustries'),
        widget=atapi.MultiSelectionWidget(
            label=_(u'label_psc_industry_cat', default=u'Industry'),
            description=_(u'help_services_industry', default=u'Select a industry from the below list.'),
            i18n_domain='ploneservicescenter',
        ),
        required=0,
        vocabulary='getIndustryVocabulary',
        index=('KeywordIndex:schema',),
    ),

    public.LinkField(
        'url',
        widget=public.LinkWidget(
            label=_(u'label_services_url', default=u'URL'),
            description=_(u'help_services_url', default=u'Enter the web address (URL). You can copy & paste this from a browser window.'),
            i18n_domain='ploneservicescenter',
        ),
        required=1,
    ),

    atapi.IntegerField(
        'rating',
        widget=atapi.SelectionWidget(
            label=_(u'label_services_rating', default=u'Rating'),
            description=_(u'help_services_rating', default=u'Select a value of options from the below list by rating.'),
            format='select',
            i18n_domain='ploneservicescenter',
        ),
        required=1,
        default=2,
        vocabulary=atapi.IntDisplayList([(i, i) for i in range(1, 4)]),
        write_permission='Manage portal',
        index=('FieldIndex:schema',),
    ),

    atapi.StringField(
        'contactName',
        widget=atapi.StringWidget(
            label=_(u'label_services_contactname', default=u'Contact Name'),
            description=_(u'help_services_contactname', default=u'Enter the contact name.'),
            i18n_domain='ploneservicescenter',
        ),
        required=0,
        searchable=1,
        index=('KeywordIndex:schema',),
    ),

    public.EmailField(
        'contactEmail',
        widget=public.EmailWidget(
            label=_(u'label_services_email', default=u'Email'),
            description=_(u'help_services_email', default=u'Enter the email for contacts.'),
            i18n_domain='ploneservicescenter',
        ),
        required=0,
        searchable=1,
        index=('KeywordIndex:schema',),
    ),

    atapi.ComputedField(
        'sortExpression',
        expression='''\
str(context.getRating()) + " " + str(context.Title()).lower()''',
        mode='r',
        index=('FieldIndex',),
        widget=atapi.StringWidget(
            label=_(u'', default=u'Sort Expression'),
            # description=_(u'', default=u''),
            visible={'edit': 'invisible', 'view': 'invisible'},
        ),
    ),



))


class BaseServicesContent(base.ATCTContent):

    _getPossibleRatings = lambda x: range(1, 4)

    global_allow = 0
    _at_rename_after_creation = True

    allow_discussion = True

    def canSeeProvider(self):
        """
        Check if we are allowed to see the provider of the site
        """
        provider = self.getProvider()
        if not provider:
            return False
        user = getSecurityManager().getUser()
        return user.has_permission('View', provider)

    def getProvidersReferences(self):
        """
        Return a sorted list of references
        """
        field = self.getWrappedField('provider')
        providers = list(field._Vocabulary(self).items())
        providers.sort(lambda a, b: cmp(a[1].lower(), b[1].lower()))
        return atapi.DisplayList(providers)

    def getCountry(self, **kw):
        # BBB lowercase to tolerate uppercase values from plone.net
        value = self.getField('country').get(self, **kw)
        if isinstance(value, (str, unicode)):
            return value.lower()
        return value
