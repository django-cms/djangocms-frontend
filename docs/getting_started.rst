#################
Getting started
#################

.. index::
    single: Installation

**************
Installation
**************

Install package
===============

For a manual install run ``pip install djangocms-frontend``

Alternatively, add the following line to your project's
``requirements.txt``:

.. code::

   djangocms-frontend


Make apps available to your django project
==========================================

Add the following entries to your ``INSTALLED_APPS``:

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
      'djangocms_frontend.contrib.image',
      'djangocms_frontend.contrib.jumbotron',
      'djangocms_frontend.contrib.link',
      'djangocms_frontend.contrib.listgroup',
      'djangocms_frontend.contrib.media',
      'djangocms_frontend.contrib.tabs',
      'djangocms_frontend.contrib.utilities',

Create necessary database table
===============================

Finally, run ``python manage.py migrate``

**djangocms-frontend** now is ready for use!

Adding styles and javascript manually
=====================================

django CMS frontend **does not** automatically add the styles or
javascript files to your frontend, these need to be added at your
discretion.

Out of the box, **djangocms-frontend** is configured to work with
`Bootstrap 5 <https://getbootstrap.com/>`_. Styles should be added to
your ``<head>`` section of your project template (often called
``base.html``). Javascript should be added at the end of the ``<body>``
section or your template. For illustration and an easier start,
**djangocms-frontend** comes with example templates.


.. index::
    single: base.html

Using example templates of djangocms-frontend
=============================================

**djangocms-frontend** comes with example templates. The simplest way to
activate `Bootstrap 5 <https://getbootstrap.com/>`_ is by using the
following base template (``base.html``)

.. code::

   {% extends "bootstrap5/base.html" %}
   {% block brand %}<a href="/">My Site</a>{% endblock %}

.. note::

    We recommend developing your own ``base.html`` for your projects. The
    example templates load CSS and JS files from a CDN. Good reasons to do so
    are

    * **djangocms-frontend** does not contain CSS or JS files from Bootstrap
      or any other framework for that matter. The example tempaltes load
      CSS and JS from a CDN.
    * It is considered safer to host CSS and JS files yourself. Otherwise you
      do not have control over the CSS and/or JS that is delivered.
    * It is a common practice to customize at least the CSS part, e.g. with
      brand colors.


The example template is customizable by a set of template blocks:

``{% block title %}``
    Renders the page title. Defaults to ``{% page_attribute "page_title" %}``

``{% block content %}``
    Here goes the main content of the page. The default setup is a ``<section>``
    with a placeholder called "Page Content" and a ``<footer>`` with a static
    placeholder (identical on all pages) called "Footer":

    .. code::

        {% block content %}
            <section>
                {% placeholder "Page Content" %}
            </section>&nbsp;
            <footer>
                {% static_placeholder "Footer" %}
            </footer>
        {% endblock content %}

``{% block navbar %}``
    This block renders a navigation bar using the Bootstrap 5 ``navbar`` classes
    and django CMS' menu system. If you need to add additional navigation on
    the right hand side of the nav bar populate the block ``searchbar``
    (which can include a search function but does not have to). Also, the block
    ``brand`` is rendered in the navigation bar.

``{% block base_css %}``
    Loads the framework's CSS. Replace this block if you prefer to include your
    the CSS from your server.

``{% block base_js %}``
    Loads the framework's JS. Replace this block if you prefer to include your
    the JS from your server. JS is loaded **before** ``{% render_block 'js' %}``.

``{% block end_js %}``
    Loads additional JS at the end of the page. Currently empty. This block
    is loaded **after** ``{% render_block 'js' %}``.

``{% block bottom_css %}``
    Additional CSS placed just before the end of the ``<body>``. Currently empty.

``{% block meta %}``
    Contains the meta description of the page. Defaults to:

    .. code::

        <meta name="description" content="{% page_attribute meta_description %}"/>
        <meta property="og:type" content="website"/>
        <meta property="og:title" content="{% page_attribute "page_title" %}"/>
        <meta property="og:description" content="{% page_attribute meta_description %}"/>

``{% block canonical_url %}``
    Contains the canonical url of the page. Defaults to:

    .. code::

        <link rel="canonical" href="{{ request.build_absolute_uri }}"/>
        <meta property="og:url" content="{{ request.build_absolute_uri }}"/>





Granting rights
===============

If you have restricted rights for users our groups in your projects make
sure that editors have the right to to add, change, delete, and - of
course - view instances of djangocms_frontend UI item.

Otherwise the plugins will not appear in the editors' frontend.


.. index::
    single: Migration from Bootstrap 4
    single: migrate_frontend
    single: manage.py migrate_frontend

.. _Migrating from djangocms-bootstrap4:

*************************************
 Migrating from djangocms-bootstrap4
*************************************

In the case you have a running django CMS project using
`djangocms-bootstrap4
<https://github.com/django-cms/djangocms-bootstrap4>`_ you can try to
run the automatic migration process. This process converts all plugin
instances of djangocms-bootstrap4 into corresponding djangocms-frontend
plugins.

.. note::

   Bootstrap 4 and Bootstrap 5 differ, hence even a  successful
   migration will require manual work to fix differences. The migration
   command is a support to reduce the amount of manual work. It will not
   do everything automatically!

   The more your existing installation uses the attributes field (found
   in "advanced settings") the more likely it is, that you will have to
   do some manual adjustment. While the migration command does adjust
   settings in the attributes field it cannot know the specifics of
   your project.

.. attention::

   Please do **back up** your database before you do run the management
   command!

For this to work, the both the djangocms-frontend **and** the
djangocms-bootstrap4 apps need to be included in ``INSTALLED_APPS``.

.. code::

   ./manage.py migrate_frontend

After you finish the migration you can remove all djangocms-bootstrap4
apps from ``INSTALLED_APPS`` and you may delete the now empty database
tables of djangocms-bootstrap4. You identify them by their name pattern:

.. code::

   bootstrap4_alerts_bootstrap4alerts
   bootstrap4_badge_bootstrap4badge
   ...
   bootstrap4_utilities_bootstrap4spacing



