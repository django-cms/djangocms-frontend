.. _built_in_components:

######################################
Installation and Usage with Built-In Components
######################################

.. index::
    single: Built-In Components
    single: Bootstrap 5 Components


Here's a step-by-step tutorial to get you started with ``djangocms-frontend``, a versatile plugin bundle
for django CMS that provides a suite of frontend components compatible with various CSS frameworks, including Bootstrap 5.

For this tutorial we will be using the built-in Boostrap 5 components that come with ``djangocms-frontend``.

Installation
============

To install ``djangocms-frontend``, follow these steps:

1. **Install the package using pip:**

   .. code-block:: bash

      pip install djangocms-frontend

   Alternatively, you can add ``djangocms-frontend`` to your ``requirements.txt`` file and install it via:

   .. code-block:: bash

      pip install -r requirements.txt

2. **Install optional dependencies (if needed):**

   Depending on your project's requirements, you may need additional dependencies:

   - For icon support with djangocms-icon and not the build-in icon plugin:

     .. code-block:: bash

        pip install djangocms-frontend[djangocms-icon]

   - To include the Ace code editor in static files (if, e.g., your project does not have
     access to the internet where django CMS loads static ace from a CDN):

     .. code-block:: bash

        pip install djangocms-frontend[static-ace]

   - To install multiple optional dependencies at once:

     .. code-block:: bash

        pip install djangocms-frontend[static-ace,djangocms-icon]


Configuration
=============

1. **Add Installed Apps**

   Open your Django project's ``settings.py`` and add the following applications to ``INSTALLED_APPS`` -
   you only need (and should) add the components you want content editors to use:

    .. code-block:: python

        INSTALLED_APPS = [
            # Optional dependencies
            'djangocms_icon',
            'easy_thumbnails',
            'djangocms_link',  # Required if djangocms_frontend.contrib.link is used
            # Main frontend components
            'djangocms_frontend',
            'djangocms_frontend.contrib.accordion',
            'djangocms_frontend.contrib.alert',
            'djangocms_frontend.contrib.badge',
            'djangocms_frontend.contrib.card',
            'djangocms_frontend.contrib.carousel',
            'djangocms_frontend.contrib.collapse',
            'djangocms_frontend.contrib.component',
            'djangocms_frontend.contrib.content',
            'djangocms_frontend.contrib.grid',
            'djangocms_frontend.contrib.icon',
            'djangocms_frontend.contrib.image',
            'djangocms_frontend.contrib.jumbotron',
            'djangocms_frontend.contrib.link',
            'djangocms_frontend.contrib.listgroup',
            'djangocms_frontend.contrib.media',
            'djangocms_frontend.contrib.tabs',
            'djangocms_frontend.contrib.utilities',
      ]

    For example, if you don't want to use any built-in components because you plan on 
    :ref:`building your own <custom_components>`, a minimal setup of ``INSTALLED_APPS`` 
    would look like this:

    .. code-block:: python

        INSTALLED_APPS = [
            'easy_thumbnails',
            'djangocms_link',  # Required if djangocms_frontend.contrib.link is used
            # Main frontend app - pre-built components not needed
            'djangocms_frontend',
        ]



2. **Apply Migrations**

   Run the following command to create the necessary database tables:

   .. code-block:: bash

      python manage.py migrate


Adding Styles and JavaScript
============================

``djangocms-frontend`` does not automatically include CSS or JavaScript files.
You need to manually add them to your templates.


.. index::
    single: base.html


1. **Using Bootstrap 5 templates (recommended to get started quickly)**

   The package is designed to work with Bootstrap 5 by default. If you want to use Bootstrap 5,
   extend the default template like this:

   .. code-block:: django

      {% extends "bootstrap5/base.html" %}
      {% block brand %}<a href="/">My Site</a>{% endblock %}

   This will load Bootstrap 5 CSS and JS from a CDN.

   .. note::

      We recommend developing your own ``base.html`` for your projects. The
      example templates load CSS and JS files from a CDN. Good reasons to do so
      are

      * ``djangocms-frontend`` does not contain CSS or JS files from Bootstrap
        or any other framework for that matter. The example templates load
        CSS and JS from a CDN.
      * It is considered safer to host CSS and JS files yourself. Otherwise you
        do not have control over the CSS and/or JS that is delivered.
      * It is a common practice to customize at least the CSS part, e.g. with
        brand colors.
      * You might have a totally different build process for your styling assets,
        especially if you use other frameworks, such as Tailwind CSS.



2. **Custom Templates**

   If you prefer to manage assets locally, download Bootstrap 5, customize as needed,
   and include it in your template:

   .. code-block:: html

      <!DOCTYPE html>
      <html lang="en">
      <head>
          <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">
      </head>
      <body>
          <script src="{% static 'js/bootstrap.bundle.min.js' %}"></script>
      </body>
      </html>

Customizing Templates
=====================

``djangocms-frontend``'s built-in templates allow for extensive customization through
Django template blocks. Some key blocks you can override:

The example template is customisable by a set of template blocks:

``{% block title %}``
    Renders the page title. Defaults to ``{% page_attribute "page_title" %}``

``{% block content %}``
    Here goes the main content of the page. The default setup is a ``<section>``
    with a placeholder called "Page Content":

    .. code::

        {% block content %}
            <section>
                {% placeholder "Page Content" %}
            </section>
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



Assigning Permissions
=====================

If you have restricted rights for users our groups in your projects make
sure that editors have the right to add, change, delete, and - of
course - view instances of all ``djangocms_frontend`` UI items:

* Accordion
* Alert
* Badge
* Card
* Carousel
* Collapse
* Content
* Forms
* Grid
* Icon
* Image
* Jumbotron
* Link
* Listgroup
* Media
* Tabs
* Utilities

Otherwise the plugins will not be editable and will not appear in the editors'
plugin selection when adding a plugin in the frontend.

Since changing them for each of the plugins manually can become tiresome a
management command can support you.

**First** manually define the permissions for the model ``FrontendUIItem`` of
the app ``djangocms_frontend``. **Then** you can synchronize
all permissions of the installed UI items by typing

.. code-block::

    ./manage.py frontend sync_permissions users
    ./manage.py frontend sync_permissions groups

These commands transfer the permissions for ``FrontendUIItem`` to all installed
plugins for each user or group, respectively.

The first command is only necessary of you define by-user permissions. Depending
on the number of users it may take some time.

Limitations of built-in components
==================================

Built-in components are a powerful tool for content editors, especially if they are used to
using the Bootstrap CSS framework. Those components are both portable to other frameworks
and extensible (see :ref:`how-to-extend-frontend-plugins`) But they have some limitations:

* **Deep nesting**: The Bootstrap 5-based components will require some nesting, e.g., a text inside a
  card inner inside a card inside a column inside a row inside a container will be a regular example.
  For some editors this might be confusing, or at least something to get used to. Also, large plugin
  trees in the structure board are more difficult to navigate.

  So even if you are working with the Bootstrap 5 framework you might consider using a template component
  to cover typical use cases.

* **"Bootstrappyness"**: Bootstrap is a powerful framework, but contains certain potentially oppinionated
  design decisions which reflect in the type of built-in components are included with ``djangocms-frontend``.

* **Need for customization**: Most websites will require some customization of the design. To use the built-in
  components as a starting point is a good idea, but you will need to customize Bootstrap to fit your design.
  See the `Bootstrap documentation <https://getbootstrap.com/docs/5.3/customize/overview/>`_ for more information.

Next Steps
==========

Now that you have installed and configured ``djangocms-frontend``, explore additional features such as:

- Creating template components or custom frontend components.
- Using advanced layout features.
- Integrating with third-party frameworks.

For more details, refer to the official documentation: https://djangocms-frontend.readthedocs.io/en/latest/

