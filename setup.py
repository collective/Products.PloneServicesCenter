from setuptools import setup

test_require = ['plone.app.testing']


setup(
    name='Products.PloneServicesCenter',
    install_requires=[
        'Plone',
        'Products.ATCountryWidget',
        ],
    test_require=test_require,
    extras_require={'test': test_require},
)
