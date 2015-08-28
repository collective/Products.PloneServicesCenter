import os
from setuptools import setup, find_packages

version = '0.2.8'
long_description = open("README.txt").read() + '\n' + \
                   open(os.path.join("docs", "HISTORY.txt")).read()
tests_require = ['plone.app.testing']

setup(
    name='Products.PloneServicesCenter',
    version=version,
    description='A hub for information about the service options and deployments for Plone',
    long_description=long_description,
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
    keywords='hub information service deployments Plone',
    maintainer='Alex Clark',
    maintainer_email='aclark@aclark.net',
    url='https://github.com/collective/Products.PloneServicesCenter',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'Plone',
        'Products.ArchAddOn',
        ],
    tests_require=tests_require,
    # extras_require={'test': tests_require},
    extras_require={
        'test': [
            'plone.app.robotframework',
            'plone.app.testing [robot] >=4.2.2',
            'plone.browserlayer',
            'plone.testing',
            'robotsuite',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
