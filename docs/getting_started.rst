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

For a manual install run ``pip install
https://github.com/fsbraun/djangocms-frontend/archive/master.zip``

Alternatively, add the following line to your project's
``requirements.txt``:

.. code::

   https://github.com/fsbraun/djangocms-frontend/archive/master.zip

.. warning::

   This installs directly from the current development tree of
   **djangocms-frontend**. **djangocms-frontend** currently is not yet
   suitable for production. Make sure to install a released version as
   soon as one becomes available. Please regularly check pypi.

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
      'djangocms_frontend.contrib.jumbotron',
      'djangocms_frontend.contrib.link',
      'djangocms_frontend.contrib.listgroup',
      'djangocms_frontend.contrib.media',
      'djangocms_frontend.contrib.picture',
      'djangocms_frontend.contrib.tabs',
      'djangocms_frontend.contrib.utilities',

Create necessary database table
===============================

Finally, run ``python manage.py migrate``

**djangocms-frontend** now is ready for use!

django CMS frontend **does not** automatically add the styles or
javascript files to your frontend, these need to be added at your
discretion.

Adding styles and javascript manually
=====================================

Out of the box, **djangocms-frontend** is configured to work with
`Bootstrap 5 <https://getbootstrap.com/>`_. Styles should be added to
your ``<head>`` section of your project template (often called
``base.html``). Javascript should be added at the end of the ``<body>``
section or your template.

Using example templates of djangocms-frontend
=============================================

**djangocms-frontend** comes with example templates. The simplest way to
activate `Bootstrap 5 <https://getbootstrap.com/>`_ is by using the
following base template (``base.html``)

.. code::

   {% extends "bootstrap5/bootstrap5.html" %}
   {% block site_title %}<a href="/">My Site</a>{% endblock %}

Granting rights
===============

If you have restricted rights for users our groups in your projects make
sure that editors have the right to to add, change, delete, and - of
course - view instances of djangocms_frontend UI Item.

.. index::
    single: Migration from Bootstrap 4

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

   Bootstrap 4 and Bootstrap 5 differ, so even a most successful
   migration will require manual work to fix differences. the migration
   command is a support to reduce the amount of manual work. It will not
   do everything automatically!

   The more your existing installation uses the attributes field (found
   in "advanced settings") the more likely it is, that you will have to
   do some manual adjustment. While the migration command does adjust
   settings in the attributes field but it cannot know the specifics of
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


.. index::
    single: Plugins

**************
 Grid plugins
**************

All plugins are listed in the section "Frontend" when adding a plugin to
a placeholder:

.. image:: screenshots/add_plugin.png

For details on how grids work, see, e.g. the `Bootstrap 5 documentation
<https://getbootstrap.com/docs/5.1/layout/grid/>`_.

.. index::
    single: Container

Container
=========

A container is an invisible element that wraps other content. There are
in two types of containers:

Fluid container
   A fluid container occupies the full width available - no matter how
   wide the viewport (or containing) element is.

Container
   All other containers restrict the width of their content depending on
   the used device. If prefixed by a size (sm, md, lg, xl) then the
   container will be fluid below the respective breakpoint.

.. image:: screenshots/container.png

.. index::
    single: Row

Row
===

A row contains one or more columns. By default columns are displayed
next to each other.

To automatically create not only a row but also some columns within that
row, enter the number of columns you will be using. You can always later
add more columns to the row or delete columns from the row.

Vertical alignmend defines how columns of different height are
positioned against each other.

Horizontal alignment defines how columns **that do not fill an entire
row** are distributed horizontally.

The section "Row-cols settings" defines how many columns should be next
to each other for a given display size. The "row-cols" entry defines the
number of columns on mobile devices (and above if no other setting is
given), the "row-cols-xl" entry the number of columns on a xl screen.

.. image:: screenshots/row.png

.. index::
    single: Column

Column
======

The column settings is largely about how much of the grid space the
column will use horizontally. To this end, the grid is divided in
(usually) 12 strips of equal width.

Auto sizing
   If no information on the column size is given, the column will be
   autosizing. This means that all autosizing columns of a row will
   occupy the same fraction of the space left, e.g. by sized columns.

Specifically sized columns
   If you enter a number the column for the specific screen size will
   exactly have the specified width. The unit of width is one twelfth of
   the surrounding's row width.

Also, you can adjust the vertical alignment of the specific column from
the row's default setting.

Finally, you can set the alignment of the content to left (right in a
rtl environment), center or right (left in a rtl environment). This
comes handy if, e.g., the column is supposed to contain centered
content.

.. image:: screenshots/col.png

*******************
 Component plugins
*******************

``djangocms-frontend`` adds a set of plugins to Django-CMS to allow for
quick usage of components defined by the underlying css framework, e.g.
bootstrap 5.

While ``djangocoms-frontend`` is set up to become framework agnostic its
heritage from ``djangocms-bootstrap4`` is intentionally and quite visible.
Hence  for the timne being, this documentation references the Bootstrap 5
documentation.

.. index::
    single: Accordion

Accordion component
===================

Build vertically collapsing sections using accordions:

.. image:: screenshots/accordion-example.png

Accordions consist of an Accordion plugin which has an Accordion Item plugin for
each collapsable section.

.. image:: screenshots/accordion-plugins.png
    :width: 394

Also see Bootstrap 5 `Accordion <https://getbootstrap.com/docs/5.0/components/accordion/>`_
documentation.

.. index::
    single: Alert

Alert component
===============

Alerts provide contextual feedback messages for typical user actions with a
handful of available alert messages.

.. image:: screenshots/alert-example.png

Alerts can be marked dismissible which implies that a close button is added on
the right hand side.

.. image:: screenshots/alert-plugins.png
    :width: 391

Also see Bootstrap 5 `Alerts <https://getbootstrap.com/docs/5.0/components/alerts/>`_
documentation.

.. index::
    single: Badge

Badge component
===============

Badges are small count and labeling components usually in headers and buttons.

While often useful if populated automatically as opposed to statically in a
plugin, badges are useful, e.g., to mark featured or new headers.

.. image:: screenshots/badge-example.png
    :width: 180

Also see Bootstrap 5 `Badge <https://getbootstrap.com/docs/5.0/components/badge/>`_
documentation.

.. index::
    single: Card

Card component
==============

Also see Bootstrap 5 `Card <https://getbootstrap.com/docs/5.0/components/card/>`_
documentation.

.. index::
    single: Carousel

Carousel component
==================

A `Carousel <https://getbootstrap.com/docs/5.0/components/carousel/>`_
is a set of images (pontentially with some description) that slide in
(or fade in) one after the other after a certain amount of time.

Collapse component
==================

The `Collapse <https://getbootstrap.com/docs/5.0/components/collapse/>`_
hides text behind its headline and offers the user a trigger (e.g., a
button) to reveal itself.

.. index::
    single: Jumbotron

Jumbotron component
===================

.. index::
    single: Link
    single: Button

Link / Button component
=======================

Media component
===============

.. index::
    single: Picture
    single: Image

Picture / image component
=========================

.. index::
    single: Spacing
    single: Spacer

Spacing component
=================

.. index::
    single: Blockquote

Blockquote component
====================

.. index::
    single: Code

Code component
==============

.. index::
    single: Figure

Figure component
================

.. index::
    single: Tabs

Tabs component
==============

-  `Content (Blockquote, Code, Figure)
   <https://getbootstrap.com/docs/5.0/content/>`_
-  `Grid (Container, Row, Column)
   <https://getbootstrap.com/docs/5.0/layout/grid/>`_
-  `Jumbotron
   <https://getbootstrap.com/docs/5.0/components/jumbotron/>`_
-  `Link / Button
   <https://getbootstrap.com/docs/5.0/components/buttons/>`_
-  `List group
   <https://getbootstrap.com/docs/5.0/components/list-group/>`_
-  `Media <https://getbootstrap.com/docs/5.0/layout/media-object/>`_
-  `Picture / Image
   <https://getbootstrap.com/docs/5.0/content/images/>`_
-  `Tabs <https://getbootstrap.com/docs/5.0/components/navs/#tabs>`_
-  `Utilities (Spacing) <https://getbootstrap.com/docs/5.0/utilities/>`_

*******
 Forms
*******

.. note::

   The form app is not yet finished. Please stay tuned.
