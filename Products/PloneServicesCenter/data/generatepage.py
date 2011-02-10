 # encoding: utf-8
"""
Make sure you put Zope 3's zope directory in your PYTHONPATH

"""

import sys
from zope.pagetemplate import pagetemplate
from plonenetdata import content

def getSites():
	return content


def main():
	templatefn = sys.argv[1]
	text = open(templatefn).read()
	pt = pagetemplate.PageTemplate()
	pt.pt_edit(text, 'text/html')
	print pt(content=getSites())

if __name__ == '__main__':
    main()
