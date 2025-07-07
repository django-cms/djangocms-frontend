#####################
 django CMS Frontend
#####################

|pypi| |docs| |coverage| |python| |django| |djangocms|

django CMS Frontend is a versatile plugin suite for django CMS that facilitates
the easy creation of reusable frontend components. It supports any CSS framework,
allowing developers to seamlessly integrate their preferred styling libraries.
For immediate use, it includes a comprehensive set of Bootstrap 5 components
and templates.


.. image:: preview.png

Key features
============

* **Effortless Development of Custom Components**: Create reusable frontend
  components with ease, utilizing simple templates and declarative form
  classes. These components can function both as CMS plugins and within
  standard Django templates. ​

* **Framework-Agnostic Design**: Maintain flexibility in your project's design
  by decoupling plugins from specific versions of a CSS framework. This ensures
  that updating frameworks in the future doesn't necessitate rebuilding your
  site's plugin structure. ​

* **Built-in Bootstrap 5 Components**: Access a ready-to-use collection
  of Bootstrap 5 components, streamlining the process of building responsive
  and modern interfaces. ​

* **Extensibility**: Enhance your project by creating custom components with
  minimal code. The system is designed to be extended both within individual
  projects and through separate theme applications. ​

* **Consistent User Experience**: Utilize plugins as UI components throughout
  your project, promoting a cohesive and uniform user interface. ​


Description
===========

Designed to be framework-agnostic, django CMS Frontend allows developers to
select and change CSS frameworks by adjusting project settings, eliminating
the need to reconstruct the CMS plugin tree when upgrading or switching
frameworks. It leverages `django-entangled
<https://github.com/jrief/django-entangled>`_ to store design parameters in
a common JSON field, preventing database bloat and facilitating seamless
updates to frontend features.

By providing a suite of Bootstrap 5-based components for layout structuring,
including grids, components, and forms, django CMS Frontend simplifies the
process of building responsive and structured page designs. Developers can
also create custom components with minimal code, ensuring a consistent and
efficient development experience.

It is up to you which (if any at all) pre-built components you want to include
in your project. Each set of components is a separate package you can include
in your project's ``INSTALLED_APPS``.


Contributing
============

Because this is a an open-source project, we welcome everyone to
`get involved in the project <https://www.django-cms.org/en/contribute/>`_ and
`receive a reward <https://www.django-cms.org/en/bounty-program/>`_ for their contribution.
Become part of a fantastic community and help us make django CMS the best CMS in the world.

We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

The project makes use of git pre-commit hooks to maintain code quality.
Please follow the installation steps to get `pre-commit <https://pre-commit.com/#installation>`_
setup in your development environment.

We're grateful to all contributors who have helped create and maintain
this package. Contributors are listed at the `contributors
<https://github.com/django-cms/djangocms-frontend/graphs/contributors>`_
section.

One of the easiest contributions you can make is helping to translate this addon on
`Transifex <https://www.transifex.com/divio/djangocms-frontend/dashboard/>`_.

Requirements
============

See ``REQUIREMENTS`` in the `setup.py
<https://github.com/django-cms/djangocms-frontend/blob/master/setup.py>`_
file for additional dependencies:

-  django-cms, version 3.11 or later
-  django-filer, version 1.7 or later
-  djangocms-attributes-field, version 1.0 or later
-  djangocms-text
-  djangocms-link
-  django-entangled 0.6 or later

Make sure `django Filer
<http://django-filer.readthedocs.io/en/latest/installation.html>`_ and
`django CMS Text <https://github.com/divio/djangocms-text>`_ /
`django CMS Text CKEditor
<https://github.com/divio/djangocms-text-ckeditor>`_ are installed and
configured appropriately.

**As of djangocms-frontend 2.0, djangocms-link is needed to use the Link/Button plugin.**

Installation
============

For a manual install:

-  run ``pip install djangocms-frontend``

-  add the following entries to your ``INSTALLED_APPS`` (or only those you need):

   .. code::

      'easy_thumbnails',
      'djangocms_link',  # Needed for link support

      # Base package template components and custom components
      'djangocms_frontend',

      # Add built-in Bootstrap 5 components as needed
      'djangocms_frontend.contrib.accordion',  # optional
      'djangocms_frontend.contrib.alert',  # optional
      'djangocms_frontend.contrib.badge',  # optional
      'djangocms_frontend.contrib.card',  # optional
      'djangocms_frontend.contrib.carousel',  # optional
      'djangocms_frontend.contrib.collapse',  # optional
      'djangocms_frontend.contrib.content',  # optional
      'djangocms_frontend.contrib.grid',  # optional
      'djangocms_frontend.contrib.icon',  # optional
      'djangocms_frontend.contrib.image',  # optional
      'djangocms_frontend.contrib.jumbotron',  # optional
      'djangocms_frontend.contrib.link',  # optional
      'djangocms_frontend.contrib.listgroup',  # optional
      'djangocms_frontend.contrib.media',  # optional
      'djangocms_frontend.contrib.tabs',  # optional
      'djangocms_frontend.contrib.utilities',  # optional

-  run ``python manage.py migrate``

**djangocms-frontend** has a weak dependencies on **djangocms-icon** you can
install separately or by adding an option:

.. code::

    pip install djangocms-frontend[djangocms-icon]  # Installs djangocms-icon for icon support in links


Documentation
=============

See readthedocs for the `documentation <https://djangocms-frontend.readthedocs.io>`_.

License
=======

See `LICENSE <https://github.com/django-cms/djangocms-frontend/blob/master/LICENSE>`_.

.. |pypi| image:: https://badge.fury.io/py/djangocms-frontend.svg
   :target: http://badge.fury.io/py/djangocms-frontend

.. |docs| image:: https://readthedocs.org/projects/djangocms-frontend/badge/?version=latest
    :target: https://djangocms-frontend.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/gh/fsbraun/djangocms-frontend/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/django-cms/djangocms-frontend

.. |python| image:: https://img.shields.io/pypi/pyversions/djangocms-frontend
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/djangocms-frontend/

.. |django| image:: https://img.shields.io/pypi/frameworkversions/django/djangocms-frontend
    :alt: PyPI - Django Versions from Framework Classifiers
    :target: https://www.djangoproject.com/

.. |djangocms| image:: https://img.shields.io/pypi/frameworkversions/django-cms/djangocms-frontend
    :alt: PyPI - django CMS Versions from Framework Classifiers
    :target: https://www.django-cms.org/
