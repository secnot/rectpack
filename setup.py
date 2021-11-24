from setuptools import setup

long_description = """A collection of heuristic algorithms for solving the 2D knapsack problem,
also known as the bin packing problem. In essence packing a set of rectangles into the
smallest number of bins."""

setup(
    name="rectpack",
    version="0.2.2",
    description="2D Rectangle packing library",
    long_description=long_description,
    url="https://github.com/secnot/rectpack/",
    author="SecNot",
    keywords=["knapsack", "rectangle", "packing 2D", "bin", "binpacking"],
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    packages=["rectpack"],
    zip_safe=False,
    test_suite="nose.collector",
    tests_require=["nose"],
)
