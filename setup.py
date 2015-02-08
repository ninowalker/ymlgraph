import os
from setuptools import setup, find_packages

from ymlgraph import __version__
import glob
import sys

setup(
    name="ymlgraph",
    version=__version__,
    author="Nino Walker",
    author_email="nino@livefyre.com",
    description="A YAML DSL with a python transformer for Graphviz",
    url='https://github.com/ninowalker/ymlgraph',
    license="MIT",
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=["""PyYAML>=3.10 docopt>=0.6.2 graphviz>=0.4.2""".split(" ")],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={'console_scripts': ['ymlgraph = ymlgraph.main:main']}
)


