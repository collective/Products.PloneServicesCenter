import os
from setuptools import setup, find_packages

tests_require = ['plone.app.testing']

setup(
    name='Products.PloneServicesCenter',
    version='0.2.7',
    description='A hub for information about the service options and deployments for Plone',
    long_description=open("README.txt").read() + '\n' +
        open(os.path.join("docs", "HISTORY.txt")).read(),
    maintainer='Alex Clark',
    maintainer_email='aclark@aclark.net',
    url='https://github.com/collective/Products.PloneServicesCenter',
    install_requires=[
        'Plone',
        'Products.ArchAddOn',
        'setuptools',
        ],
    tests_require=tests_require,
    extras_require={'test': tests_require},
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)"
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='GPL',
    packages=find_packages(),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
)
