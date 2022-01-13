===================
django CMS Frontend
===================

|pypi| |build| |coverage|

**django CMS Frontend** is a blugin bundle based on
**`django CMS Bootstrap 5 <https://github.com/gl-agnx/djangocms-bootstrap5>`_**.
Its objective is to provide a set of popular frontend components independent of
the currently used frontend framework such as Bootstrap, or its specific version.

The plugin are framework agnostic and the framework can be changed by adapting
your procet's settings. Also, it is designed to avoid having to rebuild your
CMS plugin tree when upgrading e.g. from one version of your frontend framework
to the next.

django CMS Frontend uses **`django-entangled <https://github.com/jrief/django-entangled>`_**
by Jacob Rief to avoid bloating your project's database with frontend framework-dependent
tables. Instead all design parameters are stored in a common JSON field and future
releases of improved frontend features will not require to rebuild your full
plugin tree.

The link plugin has been rewritten to not allow internal links to other CMS pages, but also
to other django models such as, e.g., posts of **`djangocms-blog <https://github.com/nephila/djangocms-blog>`_**. 

.. note:
    This is currently a proof of concept project.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/djangocms-bootstrap5/graphs/contributors>`_
section.

One of the easiest contributions you can make is helping to translate this addon on
`Transifex <https://www.transifex.com/projects/p/djangocms-bootstrap5/>`_.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/djangocms-bootstrap5/blob/master/setup.py>`_
file for additional dependencies:

|python| |django| |djangocms|

* Django Filer 1.7 or higher
* Django Text CKEditor 3.1 or higher

Make sure `django Filer <http://django-filer.readthedocs.io/en/latest/installation.html>`_
and `django CMS Text CKEditor <https://github.com/divio/djangocms-text-ckeditor>`_
are installed and configured appropriately.


Installation
------------

For a manual install:

* run ``pip install djangocms-bootstrap5``
* add the following entries to your ``INSTALLED_APPS``::

    'djangocms_icon',
    'djangocms_frontend',
    'djangocms_frontend.contrib.bootstrap5_alerts',
    'djangocms_frontend.contrib.bootstrap5_badge',
    'djangocms_frontend.contrib.bootstrap5_card',
    # 'djangocms_frontend.contrib.bootstrap5_carousel',
    'djangocms_frontend.contrib.bootstrap5_collapse',
    'djangocms_frontend.contrib.bootstrap5_content',
    'djangocms_frontend.contrib.bootstrap5_grid',
    'djangocms_frontend.contrib.bootstrap5_jumbotron',
    'djangocms_frontend.contrib.bootstrap5_link',
    'djangocms_frontend.contrib.bootstrap5_listgroup',
    'djangocms_frontend.contrib.bootstrap5_media',
    'djangocms_frontend.contrib.bootstrap5_picture',
    'djangocms_frontend.contrib.bootstrap5_tabs',
    'djangocms_frontend.contrib.bootstrap5_utilities',

* run ``python manage.py migrate``


Configuration
-------------

django CMS frontend **utilises** the following django CMS plugin:

* **django CMS Icon**: `Icon <https://github.com/divio/djangocms-icon>`_

Dependency on **django CMS Link** and **django CMS Picture** have been dropped.

It provides the following **standard** Bootstrap 5 components:

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

django CMS Bootstrap 5 **does not** add the styles or javascript files to your frontend, these need to be added at your discretion.


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
.. |django| image:: https://img.shields.io/badge/django-2.2,%203.0,%203.1-blue.svg
    :target: https://www.djangoproject.com/
.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.7%2B-blue.svg
    :target: https://www.django-cms.org/
