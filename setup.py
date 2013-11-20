import os
from setuptools import setup, find_packages

tests_require = ['plone.app.testing']

setup(
    name='Products.PloneServicesCenter',
    version='0.2.8',
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
    classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='GPL',
    packages=find_packages(),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
)
