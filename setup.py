#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='falcon-experiment',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='A test app using falcon',
    long_description=README,
    author='Matthew Power',
    author_email='mth.power@gmail.com',
    license='MIT',
    # url='https://github.com/mthpower/xlsx-to-nosql',
    zip_safe=True,
    install_requires=[
        'cython',
        'falcon',
        'marshmallow==2.0.0b5',
        'python-dateutil',
        'riak',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
