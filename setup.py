from setuptools import setup, find_packages

long_description="""A collection of heuristic algorithms for solving the 2D knapsack problem,
also known as the bin packing problem. In essence packing a set of rectangles into the 
smallest number of bins."""

setup(
    name='rectpack',
    version='0.2',
    description=long_description, 

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
