===================
django CMS Frontend
===================

|pypi| |build| |coverage|

**django CMS Frontend** is a blugin bundle based on
`djangocms_bootstrap5 <https://github.com/gl-agnx/djangocms-bootstrap5>`_.
Its objective is to provide a set of popular frontend components independent of
the currently used frontend framework such as Bootstrap, or its specific version.

Key features
============

* Separation of plugins from css framework, i.e., no need to rebuild you
site's plugin tree if css framework is changed in the future, e.g.,
from Bootstrap 5 to a future version

* New link plugin allowing to link to internal pages provided by other applications,
such as `djangocms-blog <https://github.com/nephila/djangocms-blog>`_.

* Nice and well-aranged admin frontend of djangocms-bootstrap4

* Management command to migrate from `djangocms_bootstrap44 <https://github.com/django-cms/djangocms-bootstrap4>`_.

* Extensible within the project and with separate project (e.g., a theme app)

Description
===========

The plugins are framework agnostic and the framework can be changed by adapting
your project's settings. Also, it is designed to avoid having to rebuild your
CMS plugin tree when upgrading e.g. from one version of your frontend framework
to the next.

django CMS Frontend uses `django-entangled <https://github.com/jrief/django-entangled>`_
by Jacob Rief to avoid bloating your project's database with css framework-dependent
tables. Instead all design parameters are stored in a common JSON field and future
releases of improved frontend features will not require to rebuild your full
plugin tree.

The link plugin has been rewritten to not allow internal links to other CMS pages, but also
to other django models such as, e.g., posts of
`djangocms-blog <https://github.com/nephila/djangocms-blog>`_.

Feedback
========

.. note::
    This is currently a proof of concept project. The project is not tested
    yet (in fact, tests do not run).

This project is in a early stage. All feedback is welcome! Please mail me at
fsbraun(at)gmx.de

.. Contributing
.. ============

.. This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

.. We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/djangocms-bootstrap5/graphs/contributors>`_
section.

.. One of the easiest contributions you can make is helping to translate this addon on
`Transifex <https://www.transifex.com/projects/p/djangocms-bootstrap5/>`_.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/djangocms-bootstrap5/blob/master/setup.py>`_
file for additional dependencies:

|python| |django| |djangocms|

*  django-cms, version 3.7 or later
*  django-filer, version 1.7 or later
*  djangocms-attributes-field, version 1.0 or later
*  djangocms-text-ckeditor, version 3.1 or later
*  djangocms-icon, version 1.4 or later
*  django-select2",
*  django-entangled


Make sure `django Filer <http://django-filer.readthedocs.io/en/latest/installation.html>`_
and `django CMS Text CKEditor <https://github.com/divio/djangocms-text-ckeditor>`_
are installed and configured appropriately.


Installation
------------

For a manual install:

* run ``pip install https://github.com/fsbraun/djangocms-frontend/archive/master.zip``
* add the following entries to your ``INSTALLED_APPS``::

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

* run ``python manage.py migrate``


Configuration
-------------

django CMS frontend **utilises** the following django CMS plugin:

* **django CMS Icon**: `Icon <https://github.com/divio/djangocms-icon>`_

Dependency on **django CMS Link** and **django CMS Picture** have been dropped.

Currently, it provides the following **standard** components, all available for
the Bootstrap 5 framework:

* `Accordion <https://getbootstrap.com/docs/5.0/components/accordion/>`_
* `Alerts <https://getbootstrap.com/docs/5.0/components/alerts/>`_
* `Badge <https://getbootstrap.com/docs/5.0/components/badge/>`_
* `Card <https://getbootstrap.com/docs/5.0/components/card/>`_
* `Carousel <https://getbootstrap.com/docs/5.0/components/carousel/>`_
* `Collapse <https://getbootstrap.com/docs/5.0/components/collapse/>`_
* `Content (Blockquote, Code, Figure) <https://getbootstrap.com/docs/5.0/content/>`_
* `Grid (Container, Row, Column) <https://getbootstrap.com/docs/5.0/layout/grid/>`_
* `Jumbotron <https://getbootstrap.com/docs/5.0/components/jumbotron/>`_
* `Link / Button <https://getbootstrap.com/docs/5.0/components/buttons/>`_
* `List group <https://getbootstrap.com/docs/5.0/components/list-group/>`_
* `Media <https://getbootstrap.com/docs/5.0/layout/media-object/>`_
* `Picture / Image <https://getbootstrap.com/docs/5.0/content/images/>`_
* `Tabs <https://getbootstrap.com/docs/5.0/components/navs/#tabs>`_
* `Utilities (Spacing) <https://getbootstrap.com/docs/5.0/utilities/>`_

django CMS frontend **does not** add the styles or javascript files to your
frontend, these need to be added at your discretion.


Settings
~~~~~~~~

There are various settings possible on django CMS Bootstrap 5, to restrict them
for now only the following can be changed::

    DJANGOCMS_BOOTSTRAP5_TAG_CHOICES = ['div', 'section', 'article', 'header', 'footer', 'aside']

    DJANGOCMS_BOOTSTRAP5_CAROUSEL_TEMPLATES = (
        ('default', _('Default')),
    )

    DJANGOCMS_BOOTSTRAP5_GRID_SIZE = 12
    DJANGOCMS_BOOTSTRAP5_GRID_CONTAINERS = (
        ('container', _('Container')),
        ('container-fluid', _('Fluid container')),
    )
    DJANGOCMS_BOOTSTRAP5_GRID_COLUMN_CHOICES = (
        ('col', _('Column')),
        ('w-100', _('Break')),
        ('', _('Empty'))
    )

    DJANGOCMS_BOOTSTRAP5_USE_ICONS = True

    DJANGOCMS_BOOTSTRAP5_TAB_TEMPLATES = (
        ('default', _('Default')),
    )

    DJANGOCMS_BOOTSTRAP5_SPACER_SIZES = (
        ('0', '* 0'),
        ('1', '* .25'),
        ('2', '* .5'),
        ('3', '* 1'),
        ('4', '* 1.5'),
        ('5', '* 3'),
    )

    DJANGOCMS_BOOTSTRAP5_CAROUSEL_ASPECT_RATIOS = (
        (16, 9),
    )

    DJANGOCMS_BOOTSTRAP5_COLOR_STYLE_CHOICES = (
        ('primary', _('Primary')),
        ('secondary', _('Secondary')),
        ('success', _('Success')),
        ('danger', _('Danger')),
        ('warning', _('Warning')),
        ('info', _('Info')),
        ('light', _('Light')),
        ('dark', _('Dark')),
        ('custom', _('Custom')),
    )

Please be aware that this package does not support djangocms-text-ckeditor's
`Drag & Drop Images <https://github.com/divio/djangocms-text-ckeditor/#drag--drop-images>`_
so be sure to set ``TEXT_SAVE_IMAGE_FUNCTION = None``.


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test

To run the frontend make sure to use **node 10.x**.


.. |pypi| image:: https://badge.fury.io/py/djangocms-bootstrap5.svg
    :target: http://badge.fury.io/py/djangocms-bootstrap5
.. |build| image:: https://travis-ci.org/divio/djangocms-bootstrap5.svg?branch=master
    :target: https://travis-ci.org/divio/djangocms-bootstrap5
.. |coverage| image:: https://codecov.io/gh/divio/djangocms-bootstrap5/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/divio/djangocms-bootstrap5

.. |python| image:: https://img.shields.io/badge/python-3.5+-blue.svg
    :target: https://pypi.org/project/djangocms-bootstrap5/
.. |django| image:: https://img.shields.io/badge/django-2.2,%203.0,%203.1,%203.2-blue.svg
    :target: https://www.djangoproject.com/
.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.7%2B-blue.svg
    :target: https://www.django-cms.org/
