#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
  readme = readme_file.read()

with open('requirements.in') as requirements_file:
    requirements = requirements_file.read().splitlines()


setup(
    name='footballing',
    version='0.1.0',
    packages=find_packages(include=['utils', 'utils.*']),
    install_requires=requirements,
)
