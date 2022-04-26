#!/usr/bin/env python
from setuptools import find_packages, setup

from djangocms_frontend import __version__

REQUIREMENTS = [
    "Django>=2.2,<4",
    "django-cms>=3.7",
    "django-filer>=1.7",
    "djangocms-attributes-field>=1",
    "djangocms-text-ckeditor>=3.1.0",
    "djangocms-icon>=1.4.0",
    "django-select2",
    "django-entangled==0.4",
]

EXTRA_REQUIREMENTS = {
    "reCaptcha": [
        "django-recaptcha",
    ]
}

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Framework :: Django",
    "Framework :: Django :: 2.2",
    "Framework :: Django :: 3.2",
    "Framework :: Django CMS",
    "Framework :: Django CMS :: 3.8",
    "Framework :: Django CMS :: 3.9",
    "Framework :: Django CMS :: 3.10",
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
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite="run_tests.run",
)
