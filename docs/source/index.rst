################################################
 Welcome to djangocms-frontend's documentation!
################################################

********************
 djangocms-frontend
********************

django CMS Frontend is a versatile plugin suite for django CMS that facilitates
the easy creation of reusable frontend components. It supports any CSS framework,
allowing developers to seamlessly integrate their preferred styling libraries.
For immediate use, it includes a comprehensive set of Bootstrap 5 components
and templates.


.. image:: ../../preview.png


**************
 Key features
**************

* **Effortless Development of Custom Frontend Components**: Create reusable frontend
  components with ease, utilizing simple templates and declarative form
  classes. These components can function both as CMS plugins and within
  standard Django templates.

* **Framework-Agnostic Design**: Maintain flexibility in your project's design
  by decoupling plugins from specific versions of a CSS framework. This ensures
  that updating frameworks in the future doesn't necessitate rebuilding your
  site's plugin structure.

* **Built-in Bootstrap 5 Components**: Access a ready-to-use collection
  of Bootstrap 5 components, streamlining the process of building responsive
  and modern interfaces.

* **Extensibility**: Enhance your project by creating custom frontend components with
  minimal code. The system is designed to be extended both within individual
  projects and through separate theme applications.

* **Consistent User Experience**: Utilize plugins as UI components throughout
  your project, promoting a cohesive and uniform user interface.

*************
 Description
*************

Designed to be framework-agnostic, django CMS Frontend allows developers to
select and change CSS frameworks by adjusting project settings, eliminating
the need to reconstruct the CMS plugin tree when upgrading or switching
frameworks. It leverages `django-entangled
<https://github.com/jrief/django-entangled>`_ to store design parameters in
a common JSON field, preventing database bloat and facilitating seamless
updates to frontend features.

By providing a suite of Bootstrap 5-based components for layout structuring,
including grids, components, and forms, django CMS Frontend simplifies the
process of building responsive and structured page designs. Developers can
also create custom frontend components with minimal code, ensuring a consistent and
efficient development experience.

It is up to you which (if any at all) pre-built components you want to include
in your project. Each set of components is a separate package you can include
in your project's ``INSTALLED_APPS``.


Contents
========

.. toctree::
   :maxdepth: 2

   tutorial/index
   plugins/index
   how-to/index
   reference

.. toctree::
   :hidden:

   genindex

Indices and tables
==================

-  :ref:`genindex`
-  :ref:`search`
