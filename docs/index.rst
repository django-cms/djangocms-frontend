..
   djangocms-blog documentation master file, created by
   sphinx-quickstart on Sun Jun  5 23:27:04 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

################################################
 Welcome to djangocms-frontend's documentation!
################################################

********************
 djangocms-frontend
********************

**djangocms-frontend** is a blugin bundle based on `djangocms_bootstrap5
<https://github.com/gl-agnx/djangocms-bootstrap5>`_. Its objective is to
provide a set of popular frontend components independent of the
currently used frontend framework such as Bootstrap, or its specific
version.

.. image:: ../preview.png

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

**djangocms-frontend** provides a set of plugins to structure your
layout. This includes three basic elements

The grid
   The grid is the basis for responsive page design. It splits the page
   into containers, rows and columns. Depending on the device, columns
   are shown next to each other (larger screens) or one below the other
   (smaller screens).

Components
   Components structure information on your site by giving them an easy
   to grasp and easy to use look. Alerts or cards are examples of
   components.

Forms (work in progress)
   Finally, djangocms-frontend lets you display forms in a nice way.
   Also, it handles form submit actions, validation etc. Forms can be
   easily structured using fieldsets known from django's admin app. But
   djangocms-frontend also works with third-party apps like
   `django-crispy-forms
   <https://github.com/django-crispy-forms/django-crispy-forms>`_ for
   even more complex layouts.

Contents
========

.. toctree::
   :maxdepth: 3

   getting_started
   howto_guides
   reference

.. toctree::
   :hidden:

   genindex

Indices and tables
==================

-  :ref:`genindex`
-  :ref:`search`
