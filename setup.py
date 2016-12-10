from setuptools import setup, find_packages


setup(
    name='rectpack',
    version='0.1',
    description='2D Rectangle packing library',
    
    # Main homepage
    url='https://github.com/secnot/rectpack/',
    
    # Extra info and author details
    author='SecNot',

    keywords=['knapsack', 'rectangle', 'packing 2D', 'bin', 'binpacking'],

    license='GPLv2',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        ],

    # package
    packages = ['rectpack'],
    install_requires = ['nose', 'unittest2'],
    zip_safe = False,

    # Tests
    test_suite='nose.collector',
    tests_require=['nose'],
)
