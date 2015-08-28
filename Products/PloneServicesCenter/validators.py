# -*- coding: utf-8 -*-

# from Products.PloneServicesCenter import PSCMessageFactory as _
from Products.validation.interfaces.IValidator import IValidator
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

_ = MessageFactory('ploneservicescenter')


class IndustriesValidator:
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if len([v for v in value if v]) > 2:
            return _(u'Please select at most two industries')
        return True
