#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='cluster_commander',
    version='0.1.0',
    description='A program to run commands on a cluster',
    author='Joseph Lynch',
    author_email='jolynch@mit.edu',
    url='https://github.com/jolynch/cluster_commander.git',
    packages=find_packages(exclude=['tests', 'bin']),
    include_package_data=True,
    setup_requires=['setuptools'],
    install_requires=[
        "pytest"
    ],
    license='MIT License'
)
