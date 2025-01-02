################################################
 Welcome to djangocms-frontend's documentation!
################################################

********************
 djangocms-frontend
********************

**django CMS Frontend** is a powerful plugin suite designed to streamline the
integration of frontend frameworks into django CMS. Out of the box, it provides
comprehensive support for Bootstrap 5, while also enabling the use of other
CSS frameworks, such as Tailwind CSS, through custom components.
Whether you're building responsive layouts or highly customized designs,
django CMS Frontend is designed to simplify your development workflow.

.. image:: preview.png


**************
 Key features
**************

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


*************
 Description
*************

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

Contents
========

.. toctree::
   :maxdepth: 3

   getting_started
   grid
   components
   custom_components
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
