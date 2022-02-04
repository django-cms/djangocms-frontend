#####################
 django CMS Frontend
#####################

|pypi| |coverage|

**django CMS Frontend** is a blugin bundle based on
`djangocms_bootstrap5
<https://github.com/gl-agnx/djangocms-bootstrap5>`_. Its objective is to
provide a set of popular frontend components independent of the
currently used frontend framework such as Bootstrap, or its specific
version.

.. image:: preview.png

**************
 Key features
**************

-  Support of `Bootstrap 5 <https://getbootstrap.com>`_.

-  **Separation of plugins from css framework**, i.e., no need to
   rebuild you site's plugin tree if css framework is changed in the
   future, e.g., from Bootstrap 5 to a future version.

-  **New link plugin** allowing to link to internal pages provided by
   other applications, such as `djangocms-blog
   <https://github.com/nephila/djangocms-blog>`_.

-  **Nice and well-arranged admin frontend** of `djangocms-bootstrap4
   <https://github.com/django-cms/djangocms-bootstrap4>`_

-  Management command to **migrate from djangocms-bootstrap4**. This
   command automatically migrates all djangocms-bootstrap4 plugins to
   djangocms-frontend.

-  **Extensible** within the project and with separate project (e.g., a
   theme app)

-  **Accordion** plugin and simple **forms** plugin w/ Bootstrap-styled
   forms on your cms page.

*************
 Description
*************

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

The link plugin has been rewritten to not allow internal links to other
CMS pages, but also to other django models such as, e.g., posts of
`djangocms-blog <https://github.com/nephila/djangocms-blog>`_.

Feedback
========

This project is in a early stage. All feedback is welcome! Please
mail me at fsbraun(at)gmx.de

Also, all contributions are welcome.

..
   Contributing

..
   ============

..
   This is a an open-source project. We'll be delighted to receive your

..
   feedback in the form of issues and pull requests. Before submitting your

..
   pull request, please review our `contribution guidelines

..
   <http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain
this package. Contributors are listed at the `contributors
<https://github.com/fsbraun/djangocms-frontend/graphs/contributors>`_
section.

..
   One of the easiest contributions you can make is helping to translate this addon on

..
   `Transifex <https://www.transifex.com/projects/p/djangocms-bootstrap5/>`_.

Requirements
============

See ``REQUIREMENTS`` in the `setup.py
<https://github.com/fsbraun/djangocms-frontend/blob/master/setup.py>`_
file for additional dependencies:

|python| |django| |djangocms|

-  django-cms, version 3.7 or later
-  django-filer, version 1.7 or later
-  djangocms-attributes-field, version 1.0 or later
-  djangocms-text-ckeditor, version 3.1 or later
-  djangocms-icon, version 1.4 or later
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

-  run ``pip install
   https://github.com/fsbraun/djangocms-frontend/archive/master.zip``

-  add the following entries to your ``INSTALLED_APPS``:

   .. code::

      'djangocms_icon',
      'djangocms_frontend',
      'djangocms_frontend.contrib.accordion',
      'djangocms_frontend.contrib.alert',
      'djangocms_frontend.contrib.badge',
      'djangocms_frontend.contrib.card',
      'djangocms_frontend.contrib.carousel',
      'djangocms_frontend.contrib.collapse',
      'djangocms_frontend.contrib.content',
      'djangocms_frontend.contrib.grid',
      'djangocms_frontend.contrib.jumbotron',
      'djangocms_frontend.contrib.link',
      'djangocms_frontend.contrib.listgroup',
      'djangocms_frontend.contrib.media',
      'djangocms_frontend.contrib.picture',
      'djangocms_frontend.contrib.tabs',
      'djangocms_frontend.contrib.utilities',

-  run ``python manage.py migrate``

Documentation
=============

See readthedocs for the `currently draft documentation
<https://djangocms-frontend.readthedocs.io>`_.

.. |pypi| image:: https://badge.fury.io/py/djangocms-frontend.svg
   :target: http://badge.fury.io/py/djangocms-frontend

.. |coverage| image:: https://codecov.io/gh/fsbraun/djangocms-frontend/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/fsbraun/djangocms-frontend

.. |python| image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://pypi.org/project/djangocms-frontend/

.. |django| image:: https://img.shields.io/badge/django-3.2-blue.svg
   :target: https://www.djangoproject.com/

.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.8%2B-blue.svg
   :target: https://www.django-cms.org/
