
This directory contains some sample data and some ZPT views that are usable with
Zope 3 page templates outside Plone as described here:

  http://hathawaymix.org/Weblog/2004-10-05-01

To use this approach, you need either Zope 3. Set your PYTHONPATH environment variable to the directory *above* zope.pagetemplates.

To use this for the sample data, run a command like this:

  python ./generatepage.py templatename.html

...where 'templatename.html' is the filename of a ZPT in this directory.
