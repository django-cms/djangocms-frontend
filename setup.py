#!/usr/bin/env python
from setuptools import find_packages, setup

from djangocms_frontend import __version__

REQUIREMENTS = [
    "django-cms>=3.7",
    "django-filer>=1.7",
    "djangocms-attributes-field>=1",
    "djangocms-text-ckeditor>=3.1.0",
    "djangocms-icon>=1.4.0",
    "django-select2",
    "django-entangled>=0.4.0",
    "pre-commit",
]


CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Framework :: Django",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.0",
    "Framework :: Django :: 3.1",
    "Framework :: Django :: 3.2",
    "Framework :: Django CMS",
    "Framework :: Django CMS :: 3.7",
    "Framework :: Django CMS :: 3.8",
    "Framework :: Django CMS :: 3.9",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
]


setup(
    name="djangocms-frontend",
    version=__version__,
    author="fsbraun",
    author_email="fsbraun@gmx.de",
    url="https://github.com/fsbraun/djangocms-frontend",
    license="BSD-3-Clause",
    description="Adds abstract User Interface items as plugins.",
    long_description=open("README.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite="run_tests",
)
