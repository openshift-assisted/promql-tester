#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), name), "rt") as f:
        return f.read()

def read_reqs(name):
    return [line for line in read_file(name).split('\n') if line and not line.strip().startswith('#')]

ROOT = os.path.dirname(__file__)

if sys.version_info < (3, 6, 0):
    sys.exit("Python 3.6.0 is the minimum required version for building this package")

setup(
    name='promql-tester',
    version="0.0.1",
    description='Testing deployment condition with promQL',
    long_description=read_file('README.md'),
    author='RedHat',
    author_email='unknown',
    url='https://github.com/openshift-assisted/promql-tester',
    packages=find_packages('.'),
    package_dir={'': '.'},
    include_package_data=True,
    license="Apache License 2.0",
    zip_safe=False,
    keywords='promql test acceptance test',
    python_requires='>=3.6',
    install_requires=read_reqs('requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': ["promql_tester = promql_tester.__main__:cli"],
    },
)
