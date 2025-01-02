#####################
 django CMS Frontend
#####################

|pypi| |docs| |coverage| |python| |django| |djangocms| |djangocms4|

**django CMS Frontend** is a powerful plugin suite designed to streamline the
integration of frontend frameworks into django CMS. Out of the box, it provides
comprehensive support for Bootstrap 5, while also enabling the use of other
CSS frameworks, such as Tailwind CSS, through custom components.
Whether you're building responsive layouts or highly customized designs,
django CMS Frontend is designed to simplify your development workflow.

.. image:: preview.png

Key features
============

- **Easy to implement re-usable frontend custom components**, which in the
  simplest case consist of a template and declarative sort of form class.

- Support of `Bootstrap 5 <https://getbootstrap.com>`_, django CMS 3.8+
  and django CMS 4 out of the box.

- Support of other frameworks such as `Tailwind CSS <https://tailwindcss.com>`_
  through custom components.

- **Separation of plugins from css framework**, i.e. no need to
  rebuild you site's plugin tree if css framework is changed in the
  future, e.g. from Bootstrap 5 to a future version.

- **Plugins are re-usable as UI components** anywhere in your project
  (e.g. in a custom app) giving your whole project a more consistent
  user experience.

- **Extensible** within the project and with separate project (e.g. a
  theme app). Create your own components with a few lines of code only.



Description
===========
django CMS Frontend is framework agnostic but comes with support of selected
components of Bootstrap 5. Components can have different templates for different
frameworks and the preferred framework can be set in the project settings.

It is up to you which (if any at all) components you want to include in your
project. Each set of components is a separate package you can include in your
project's ``INSTALLED_APPS``.

The components are designed to be re-usable as UI components in your
project, e.g. in a custom app, giving your whole project a more
consistent user experience.

django CMS Frontend uses `django-entangled
<https://github.com/jrief/django-entangled>`_ by Jacob Rief to avoid
bloating your project's database with css framework-dependent tables.
Instead all design parameters are stored in a common JSON field and
future releases of improved frontend features will not require to
rebuild your full plugin tree.


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
-  django-entangled 0.6 or later

Make sure `django Filer
<http://django-filer.readthedocs.io/en/latest/installation.html>`_ and
`django CMS Text CKEditor
<https://github.com/divio/djangocms-text-ckeditor>`_ are installed and
configured appropriately.

Installation
============

For a manual install:

-  run ``pip install djangocms-frontend``

-  add the following entries to your ``INSTALLED_APPS`` (or only those you need):

   .. code::

      'easy_thumbnails',
      'djangocms_frontend',
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

.. |python| image:: https://img.shields.io/badge/python-3.7+-blue.svg
   :target: https://pypi.org/project/djangocms-frontend/

.. |django| image:: https://img.shields.io/badge/django-3.2+-blue.svg
   :target: https://www.djangoproject.com/

.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.8%2B-blue.svg
   :target: https://www.django-cms.org/

.. |djangocms4| image:: https://img.shields.io/badge/django%20CMS-4-blue.svg
   :target: https://www.django-cms.org/en/preview-django-cms-40/
