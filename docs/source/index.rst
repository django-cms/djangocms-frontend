################################################
 Welcome to djangocms-frontend's documentation!
################################################

********************
 djangocms-frontend
********************

**django CMS Frontend** is a plugin bundle which originally built on and improved
the architecture of `djangocms-bootstrap4 <https://github.com/django-cms/djangocms-bootstrap4>`_.
Its objective is to provide a toolset to quickly create re-usable frontend
components and comes preloaded with a set of popular frontend components
independent of the currently used frontend framework such as Bootstrap, or
its specific version.

.. image:: ../../preview.png

**************
 Key features
**************

- **Easy to implement re-usable frontend custom components**, which in the
  simplest case consist of a template and declarative sort of form class.

- Support of `Bootstrap 5 <https://getbootstrap.com>`_, django CMS 3.8+
  and django CMS 4 out of the box.

- **Separation of plugins from css framework**, i.e. no need to
  rebuild you site's plugin tree if css framework is changed in the
  future, e.g. from Bootstrap 5 to a future version.

- Leverage of new **djangocms-link features** allowing to link to internal pages
  provided by other applications, such as `djangocms-blog
  <https://github.com/nephila/djangocms-blog>`_.

- **Nice and well-arranged admin frontend** of djangocms-bootstrap4

- **Extensible** within the project and with separate project (e.g. a
  theme app). Create your own components with a few lines of code only.

- **Plugins are re-usable as UI components** anywhere in your project
  (e.g. in a custom app) giving your whole project a more consistent
  user experience.

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


Contents
========

.. toctree::
   :maxdepth: 3

   getting_started
   custom_components
   grid
   components
   plugins/toc
   how-to/index
   reference

.. toctree::
   :hidden:

   genindex

Indices and tables
==================

-  :ref:`genindex`
-  :ref:`search`
