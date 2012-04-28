#!/usr/bin/env python
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='zedule',
    version='0.0.1',
    description='A scheduling server',
    keywords = 'zeromq',
    url='https://github.com/philipcristiano/zedule',
    author='Philip Cristiano',
    author_email='zedule@philipcristiano.com',
    license='BSD',
    packages=['zedule'],
    install_requires=[
        'pyzmq',
    ],
    test_suite='tests',
    long_description=read('README.md'),
    zip_safe=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    entry_points="""
    [console_scripts]
    zedule = zedule.daemon:main
    """,
)
