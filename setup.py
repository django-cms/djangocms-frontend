#!/usr/bin/env python
from setuptools import find_packages, setup

from djangocms_frontend import __version__

REQUIREMENTS = [
    "django-cms>=3.7",
    "django-filer>=1.7",
    "easy-thumbnails",
    "djangocms-attributes-field>=4",
    "djangocms-link>=5",
    "django-entangled>=0.6",
]

EXTRA_REQUIREMENTS = {
    "djangocms-icon": [
        "djangocms-icon>=1.4.0",
    ],
    "static-ace": [
        "djangocms-static-ace",
    ],
    "cms-4": [
        "django-cms>=4.1.0",
        "djangocms-link>=5.0.0",
        "django-parler",
        "djangocms-versioning>=2.0.0",
        "djangocms-alias>=2.0.0",
        "djangocms-text",
    ],
    "cms-3": [
        "django-cms<4",
        "djangocms-text",
        "djangocms-link>=5.0.0",
        "django-parler",
    ],
}

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Framework :: Django",
    "Framework :: Django :: 4.2",
    "Framework :: Django :: 5.0",
    "Framework :: Django :: 5.1",
    "Framework :: Django :: 5.2",
    "Framework :: Django CMS",
    "Framework :: Django CMS :: 3.11",
    "Framework :: Django CMS :: 4.0",
    "Framework :: Django CMS :: 4.1",
    "Framework :: Django CMS :: 5.0",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
]

PROJECT_URLS = {
    "Documentation": "https://djangocms-frontend.readthedocs.io",
    "Release notes": "https://github.com/django-cms/djangocms-frontend/blob/master/CHANGELOG.rst",
    "Issues": "https://github.com/django-cms/djangocms-frontend/issues",
    "Source": "https://github.com/django-cms/djangocms-frontend",
}


setup(
    name="djangocms-frontend",
    version=__version__,
    author="fsbraun",
    author_email="fsbraun@gmx.de",
    maintainer="Django CMS Association and contributors",
    maintainer_email="info@django-cms.org",
    url="https://github.com/django-cms/djangocms-frontend",
    license="BSD-3-Clause",
    description="Adds abstract User Interface items as plugins to django CMS.",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    classifiers=CLASSIFIERS,
    project_urls=PROJECT_URLS,
    test_suite="run_tests.run",
)
