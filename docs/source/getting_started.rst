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

**djangocms-frontend** has weak dependencies you can install separately or
by adding an option:

.. code::

    djangocms-frontend[djangocms-icon]  # Installs djangocms-icon for icons support in links
    djangocms-frontend[static-ace]  # Installs djangocms-static-ace to include the ace code editor in static files
    djangocms-frontend[static-ace, djangocms-icon]  # comma-separate multiple dependencies
    djangocms-frontend[djangocms-link]  # Installs djangocms-link for link support

``djangocms-frontend[static-ace]`` is useful if your project cannot or should not
access a CDN to load the `ace code editor <https://ace.c9.io>`_ for the code plugin.
Please be sure to in this case also add ``"djangocms_static_ace"`` to your
project's ``INSTALLED_APPS``.

Make apps available to your django project
==========================================

Add the following entries to your ``INSTALLED_APPS``:

   .. code::

      "djangocms_icon",  # optional
      "easy_thumbnails",
      "djangocms_link",  # Needed for link support
      "djangocms_frontend",
      "djangocms_frontend.contrib.accordion",
      "djangocms_frontend.contrib.alert",
      "djangocms_frontend.contrib.badge",
      "djangocms_frontend.contrib.card",
      "djangocms_frontend.contrib.carousel",
      "djangocms_frontend.contrib.collapse",
      "djangocms_frontend.contrib.component",
      "djangocms_frontend.contrib.content",
      "djangocms_frontend.contrib.grid",
      "djangocms_frontend.contrib.icon",
      "djangocms_frontend.contrib.image",
      "djangocms_frontend.contrib.jumbotron",
      "djangocms_frontend.contrib.link",
      "djangocms_frontend.contrib.listgroup",
      "djangocms_frontend.contrib.media",
      "djangocms_frontend.contrib.tabs",
      "djangocms_frontend.contrib.utilities",


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
      or any other framework for that matter. The example templates load
      CSS and JS from a CDN.
    * It is considered safer to host CSS and JS files yourself. Otherwise you
      do not have control over the CSS and/or JS that is delivered.
    * It is a common practice to customize at least the CSS part, e.g. with
      brand colors.

