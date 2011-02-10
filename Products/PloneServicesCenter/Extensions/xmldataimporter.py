#!/bin/env python
"""
Convert an XML file for plone.net into Python datastructures.

Some of the people on the plone.net project are using desktop tools to
collect and organize plone.net data.  These desktop tools are capable
of producing XML, albeit in different dialects.

If these people write a converter to get their dialect into
PloneNetML, then this script can take that data and return a
dictionary of sequences of dictionaries.

Stated graphically, imagine XML that looks like this:

  items
    providers
      item
        field (e.g. id, title, etc.)
        sites
          item
            field
        casestudies
          item
            field

...then this script will produce something like this:

items = {
  'providers': [
    {'id': 'enfoldsystems',
     'title': 'Enfold Systems',
     'description': 'Enfold is the etc.',
     'country': 'US',
     etc.
     'sites': [
        {'id': 'oxfamamerica',
         'title': 'Oxfam America',
         etc.
        },
      ]
    },
    another provider dictionary here...
  ]
}

This script only relies on minidom being installed.
"""


from os.path import join
import xml.dom.minidom

# kinda config-y type things, but let's keep them here so that Paul can run the script off the FS
importfilename = "plonenetdata.xml"
fields = ("title", "id", "description", "username", "contactName", "country", "contactEmail", "url")


# zope integration
try:
    from Products.PloneServicesCenter.config import HOME_PATH_ELEMENTS
    HOME_PATH = reduce(lambda x,y:join(x,y),HOME_PATH_ELEMENTS)
    importfilepath = join(HOME_PATH, importfilename)
except ImportError:
    # we are probably Paul, running this off the filesystem instead of through Zope. 
    importfilepath = join('data', importfilename)


def getValue(node, fieldname):
    """Shortcut to grab the value of a node using the DOM"""

    for field in node.getElementsByTagName("field"):
	if field.getAttribute("name") == fieldname:	    
  	    try:
		v = field.firstChild.nodeValue
	    except AttributeError:
		v = None
	    except IndexError:
		v = None

	    # Clean up url by putting an http in front if needed
	    if (fieldname == "url") and v and (v[0:5] != "http:"):
		v = "http://" + v

	    return v

def loadItems():
    """Iterate through the nodes and create Python data structures"""

    items = []


    xmlstring = open(importfilepath, "r").read()
    
    dom = xml.dom.minidom.parseString(xmlstring)

    for item in dom.getElementsByTagName("providers")[0].childNodes:
	if item.parentNode.tagName != "providers" or item.nodeType!=1:
	    continue

	thisitem = {}
	items.append(thisitem)
	for field in fields:
	    thisitem[field] = getValue(item, field)
	
	thisitem['sites'] = []
	for sites in item.getElementsByTagName("sites"):
	    for site in sites.getElementsByTagName("item"):
		thissite = {}
		thissite['provider'] = getValue(site, 'provider')
		for field in fields:
		    thissite[field] = getValue(site, field)
		thisitem['sites'].append(thissite)

    return items

def main():
    items = loadItems()

    for provider in items:
	print provider["title"], provider["url"]
    #return items

if __name__ == "__main__": print main()

