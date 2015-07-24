#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

requirements = open("requirements.txt", "r")

setup(
    name='DynaSchema',
    version='0.0.1',
    author='Michael Newman',
    author_email='dynaschema@newmaniese.com',
    description='Creates simple schemas for Dynamo Tables',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    test_suite = 'nose.collector',
    install_requires=requirements,
    tests_require=['nose'],
    # Install these with "pip install -e '.[paging]'" or '.[docs]'
    extras_require={
        'paging': 'pycrypto>=2.6',
        'docs': 'sphinx',
    }
)
