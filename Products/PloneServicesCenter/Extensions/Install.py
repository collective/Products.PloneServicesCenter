# -*- coding: utf-8 -*-

from Products.Archetypes.public import listTypes, process_types
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.PloneServicesCenter.config import *
from Products.CMFCore.utils import getToolByName

from StringIO import StringIO

from Products.PloneServicesCenter.Extensions import xmldataimporter
from Products.PloneServicesCenter.Extensions import public_workflow, supporter_workflow, plonenet_folder_workflow
from Products.PloneServicesCenter import security
from Products.PloneServicesCenter import PSCMessageFactory as _


#   {'description': u'Testprovider is only here to show how the content import works. 
#     It is not a real provider. Replace the XML file in Extensions/data with one containing
#     real content to get proper data imported', 
#    'title': u'TestProvider', 
#    'url': u'www.testprovider.com', 
#    'country': u'SF', 
#    'contactEmail': u'john@foo.bar', 
#    'contactName': u'John Foo', 
#    'id': u'testprovider'
#    'sites': [{ 'description': u'A testsite allegdedly built by Testprovider', 
#                'title': u'A test Site', 
#                'url': u'www.testite.com', 
#                'country': u'SF', 
#                'contactEmail': None, 
#                'contactName': None, 
#                'provider': None, 
#                'id': u'testsite'}], }
#



def createInitialContent(self, out):
    """if the config says so - create initial content from the xml file in Extenstions/data"""
    if not CREATE_INITIAL_CONTENT:
        return False

    data = xmldataimporter.loadItems()
    

    if 'providers' not in self.objectIds():
        self.invokeFactory('ProviderFolder', 'providers', title='Providers')
    
    if 'buzz' not in self.objectIds():
        self.invokeFactory('BuzzFolder', 'buzz', title='Plone Buzz')

    if 'case-studies' not in self.objectIds():
        self.invokeFactory('CaseStudyFolder', 'case-studies',
                           title='Case Studies')

    if 'sites' not in self.objectIds():
        self.invokeFactory('SiteUsingPloneFolder', 'sites', title='Sites')


    for item in data:
        print item["title"]

    	if not item["id"]:
            print >>out, "XXX item missing id : %s" % str(item)
    	    continue

    	if item['id'] in self.providers.objectIds():
    	    # XXX Skip over if a provider already exists
    	    print >>out, "Skipping duplicate %s" % item["title"]
        else:
    	    self.providers.invokeFactory('Provider', **item)
            newprovider = getattr(self.providers, item['id'])
            if item.get('username'):
                newprovider.manage_setLocalRoles(item.get('username'), ('Owner',) )

            if item.has_key('sites'):
                for site in item['sites']:
                    self.sites.invokeFactory('SiteUsingPlone', **site)
                    newsite = getattr(self.sites, site['id'])
                    newsite.setProvider(newprovider)
                    if item.get('username'):
                        newsite.manage_setLocalRoles(item.get('username'), ('Owner',) )



def makeUser2(self, provider, out):
    mtool = getToolByName(self, 'portal_membership')
    userid = provider['id']
    if not mtool.getMemberById(userid):
        mtool.addMember(userid, 'changeme', roles=['Member'], domains=[], \
                        properties={'email'    :provider.get('contactEmail'), 
                                    'fullname' :provider.get('contactName').encode('utf-8')
                                    })
        print >>out, "created user for  : %s" %(provider.get('contactName')) 
    return userid

def install_portlets(self, out):
    # prepend to the left_slots list, so it appears on top for Reviewers
    self.left_slots = [ 'here/portlet_stale_items/macros/portlet',] + list(self.left_slots)
    print >>out, "Added portlet"

def install_properties(self, out):
    # Create a new properties sheet
    proptool = getToolByName(self, 'portal_properties')
    props = getattr(proptool, 'psc_properties', None)
    if props:
        return
    
    proptool.manage_addPropertySheet(id = 'psc_properties',
                                     title = 'Plone Software Center properties')
    props = proptool.psc_properties
    props.manage_addProperty('industryVocabulary',
                             [ _(u"Business"),
                               _(u"Non-profits"),
                               _(u"Education"),
                               _(u"Science"),
                               _(u"Government"),
                               _(u"Libraries"),
                               _(u"Environmental"),
                               _(u"Military")],
                             'lines')
    
    print >>out, "Added properties sheet"

def setupWorkflow(portal, out, force_reinstall=True):
    wf_tool=portal.portal_workflow
    workflows = { 'supporter_workflow': { 'title': 'supporter_workflow (Supporter Workflow)',
                                          'types': [ 'Provider', 'CaseStudy' ]},
                  'public_workflow': { 'title': 'public_workflow (Public Workflow)',
                                       'types': [ 'Buzz', 'SiteUsingPlone' ]},
                  'plonenet_folder_workflow': { 'title': 'plonenet_folder_workflow (Folder Workflow)',
                                                'types': [ 'ProviderFolder', 'BuzzFolder', 'CaseStudyFolder', 'SiteUsingPloneFolder' ] },
                  }

    exist = lambda wf: wf in wf_tool.objectIds()
    for wf in workflows.keys():
        # Delete if needed
        if exist(wf) and force_reinstall:
            wf_tool.manage_delObjects([wf])
        if not exist(wf):
            wf_tool.manage_addWorkflow(workflows[wf]["title"], wf)
            #addWorkflowScripts(wf_tool[wf])

        # Assign to Content Classes
        wf_tool.setChainForPortalTypes(workflows[wf]["types"], wf)

    wf_tool.updateRoleMappings()


def install(self):
    out = StringIO()

    types = listTypes(PROJECTNAME)
    installTypes(self, out,
                 types,
                 PROJECTNAME)

    # Enable portal_factory for the new content types
    factory = getToolByName(self, 'portal_factory')
    new_types, useless1, useless2 = process_types(types, PROJECTNAME)
    types = factory.getFactoryTypes().keys()
    for new_type in new_types:
	if new_type.portal_type not in types:
	    types.append(new_type.portal_type)
    factory.manage_setPortalFactoryTypes(listOfTypeIds=types)
    print >> out, "Added new content types to 'portal_factory'."

    # Configure the navigation
    props = self.portal_properties.navtree_properties
    types = list(props.getProperty("metaTypesNotToList", []))
    types_to_exclude = [ "Provider", "Buzz", "CaseStudy", "SiteUsingPlone" ]
    for typ in types_to_exclude:
        if not typ in types:
            types.append(typ)
    props.manage_changeProperties(metaTypesNotToList = types)

    install_subskin(self, out, GLOBALS)
    setupWorkflow(self, out)
    portal_css = getToolByName(self, 'portal_css')
    portal_css.registerStylesheet(  id='psc.css',
                                    expression='python: True', ## Not sure when we would not want this CSS...
                                    media='all',
                                    title='PSC styles',
                                    enabled=True)

    # Create the property sheet
    install_properties(self, out)

    # Setup roles
    security.setPortalDefaultPermissions(self)
    
    # Create initial content
    createInitialContent(self, out)
    return out.getvalue()



def uninstall(self):
    out = StringIO()

    # remove the stale-items portlet from the portal root object
    portletPath = 'here/portlet_stale_items/macros/portlet'
    if portletPath in self.left_slots:
        self.left_slots = [p for p in self.left_slots if (p != portletPath)]
        print >> out, 'Removed stale-items portlet'

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()

def beforeUninstall(portal, reinstall, product, cascade):
    out = StringIO()
    try:
        cascade.remove('portalobjects')
    except:
        pass
    out.write('[portal] preserved root content.\n')
    return out, cascade
