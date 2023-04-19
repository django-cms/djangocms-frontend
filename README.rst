#####################
 django CMS Frontend
#####################

|pypi| |docs| |coverage| |python| |django| |djangocms| |djangocms4|

**django CMS Frontend** is a plugin bundle which builds on and improves
the architecture of `djangocms-bootstrap4 <https://github.com/django-cms/djangocms-bootstrap4>`_.
Its objective is to provide a set of popular frontend components independent of the
currently used frontend framework such as Bootstrap, or its specific version.

.. image:: preview.png

Key features
============

-  Support of `Bootstrap 5 <https://getbootstrap.com>`_, django CMS 3.8+
   and the new upcoming major django CMS 4.

-  **Separation of plugins from css framework**, i.e. no need to
   rebuild you site's plugin tree if css framework is changed in the
   future, e.g. from Bootstrap 5 to a future version.

-  **New link plugin** allowing to link to internal pages provided by
   other applications, such as `djangocms-blog
   <https://github.com/nephila/djangocms-blog>`_.

-  **Nice and well-arranged admin frontend** of `djangocms-bootstrap4
   <https://github.com/django-cms/djangocms-bootstrap4>`_

-  A management command to **migrate from djangocms-bootstrap4**. This
   command automatically migrates all ``djangocms-bootstrap4`` plugins to
   ``djangocms-frontend``.

-  **Extensible** within the project and with separate project (e.g. a
   theme app)


Description
===========

The plugins are framework agnostic and the framework can be changed by
adapting your project's settings. Also, it is designed to avoid having
to rebuild your CMS plugin tree when upgrading e.g. from one version of
your frontend framework to the next.

django CMS Frontend uses `django-entangled
<https://github.com/jrief/django-entangled>`_ by Jacob Rief to avoid
bloating your project's database with css framework-dependent tables.
Instead all design parameters are stored in a common JSON field and
future releases of improved frontend features will not require to
rebuild your full plugin tree.

The link plugin has been rewritten to not only allow internal links to other
CMS pages, but also to other django models such as, e.g., posts of
`djangocms-blog <https://github.com/nephila/djangocms-blog>`_.

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

-  django-cms, version 3.7 or later
-  django-filer, version 1.7 or later
-  djangocms-attributes-field, version 1.0 or later
-  djangocms-text-ckeditor, version 3.1 or later
-  django-select2
-  django-entangled

Make sure `django Filer
<http://django-filer.readthedocs.io/en/latest/installation.html>`_ and
`django CMS Text CKEditor
<https://github.com/divio/djangocms-text-ckeditor>`_ are installed and
configured appropriately.

Installation
============

For a manual install:

-  run ``pip install djangocms-frontend``

-  add the following entries to your ``INSTALLED_APPS``:

   .. code::

      'easy_thumbnails',
      'djangocms_frontend',
      'djangocms_frontend.contrib.accordion',
      'djangocms_frontend.contrib.alert',
      'djangocms_frontend.contrib.badge',
      'djangocms_frontend.contrib.card',
      'djangocms_frontend.contrib.carousel',
      'djangocms_frontend.contrib.collapse',
      'djangocms_frontend.contrib.content',
      'djangocms_frontend.contrib.grid',
      'djangocms_frontend.contrib.icon',
      'djangocms_frontend.contrib.image',
      'djangocms_frontend.contrib.jumbotron',
      'djangocms_frontend.contrib.link',
      'djangocms_frontend.contrib.listgroup',
      'djangocms_frontend.contrib.media',
      'djangocms_frontend.contrib.tabs',
      'djangocms_frontend.contrib.utilities',

-  run ``python manage.py migrate``

If you use **Django < 3.2** please also add ``django-jsonfield-backport`` to
your ``requirements.txt`` and ``django_jsonfield_backport`` to your
``INSTALLED_APPS`` list.

**djangocms-frontend** has a weak dependencies on **djangocms-icon** you can
install separately or by adding an option:

.. code::

    pip install djangocms-frontend[djangocms-icon]  # Installs djangocms-icon for icon support in links



Documentation
=============

See readthedocs for the `documentation
<https://djangocms-frontend.readthedocs.io>`_.

.. |pypi| image:: https://badge.fury.io/py/djangocms-frontend.svg
   :target: http://badge.fury.io/py/djangocms-frontend

.. |docs| image:: https://readthedocs.org/projects/djangocms-frontend/badge/?version=latest
    :target: https://djangocms-frontend.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |coverage| image:: https://codecov.io/gh/fsbraun/djangocms-frontend/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/django-cms/djangocms-frontend

.. |python| image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://pypi.org/project/djangocms-frontend/

.. |django| image:: https://img.shields.io/badge/django-3.2--4.2-blue.svg
   :target: https://www.djangoproject.com/

.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.8%2B-blue.svg
   :target: https://www.django-cms.org/

.. |djangocms4| image:: https://img.shields.io/badge/django%20CMS-4-blue.svg
   :target: https://www.django-cms.org/en/preview-django-cms-40/
