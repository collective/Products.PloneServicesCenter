# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PloneServicesCenter.content import country
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound

import random


class PloneInListing(BrowserView):
    implements(IPublishTraverse)
    country = None
    country_code = None
    country_name = None
    sections = 0
    number_case_studies = 0
    number_sites = 0
    number_providers = 0
    NUMBER_SHOW = 10

    def publishTraverse(self, request, name):
        if name in self.getUniqueCountriesNames().keys():
            self.country = name
            return self
        try:
            return super(PloneInListing, self).publishTraverse(request, name)
        except NotFound:
            default = DefaultPublishTraverse(self, request)
            return default.publishTraverse(request, name)

    def countryURL(self, country):
        return ''.join(country.lower().split())

    def getUniqueCountries(self):
        """
        Return countries which at least one content of the web site
        relates with
        """
        catalog = getToolByName(self, 'portal_catalog')
        return [c for c in catalog.uniqueValuesFor('getCountry') if c]

    def getUniqueCountriesNames(self):
        """
        Return countries which at least one content of the web site
        relates with; return a sorted list of (code, name) pairs.
        """
        countries = {}
        for code in self.getUniqueCountries():
            name = country.vocab.getValue(code, code)
            countries[self.countryURL(name)] = (code, name,)
        return countries

    def _getFilteredObjects(self, country=None, **kwargs):
        """
        Get objects filtered by countries/industries if asked for,
        handling some special cases
        """
        query = {}

        #  Add countries/industries, filtering out empty ones
        if self.country_code is not None:
                query['getCountry'] = self.country_code

        #  Filter out empty/None arguments
        for key, value in kwargs.items():
            if value:
                query[key] = value

        catalog = getToolByName(self, 'portal_catalog')
        return catalog(**query)

    def getSitesUsingPlone(self, **kwargs):
        """
        Return brains of SiteUsingPlone, sorted alphabetically
        """
        result = self._getFilteredObjects(meta_type='SiteUsingPlone',
                                          sort_on='getSortExpression',
                                          **kwargs)
        self.number_sites = len(result)
        if self.number_sites > 0:
            self.sections += 1
        return random.sample(result, min(self.number_sites, self.NUMBER_SHOW))

    def getCaseStudies(self, **kwargs):
        """
        Return brains of CaseStudy, sorted alphabetically
        """
        result = self._getFilteredObjects(meta_type='CaseStudy',
                                          sort_on='getSortExpression',
                                          **kwargs)
        self.number_case_studies = len(result)
        if self.number_case_studies > 0:
            self.sections += 1
        return random.sample(result, min(self.number_case_studies, self.NUMBER_SHOW))

    def getProviders(self, **kwargs):
        """
        Get filtered providers
        """
        result = self._getFilteredObjects(meta_type='Provider',
                                          sort_on='getSortExpression',
                                          **kwargs)
        number_premium = 0
        for provider in result:
            if provider.isPremium:
                number_premium += 1
            else:
                #  all premium providers should be in the beginning of the result
                break
        self.number_providers = len(result)
        if self.number_providers > 0:
            self.sections += 1
        premium_providers = result[:number_premium]
        result = result[number_premium:]
        return random.sample(premium_providers, number_premium) + random.sample(result, min(len(result), self.NUMBER_SHOW - number_premium))

    def section_style(self):
        if self.sections == 0:
            return ''
        else:
            # return 'float:left; width:%s%%;'%(100/self.sections)
            return 'float:left; width:{0}%%;'.format(100 / self.sections)

    def __call__(self):
        countries = self.getUniqueCountriesNames()
        if self.country is not None:
            self.country_code, self.country_name = countries[self.country]
            return ViewPageTemplateFile('plonein_country.pt')(self)
        return ViewPageTemplateFile('plonein.pt')(self)
