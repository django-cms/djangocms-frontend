.. _template_components:

############################
Building Template Components
############################

.. index::
    single: Template Components
    single: Auto Components

.. versionadded:: 2.1

Custom components are a powerful tool for content editors, allowing them to build pages without needing
in-depth knowledge of design, HTML, or nested structures. Editors can simply add content to pre-defined
components, creating visually cohesive pages with ease.

When working with `Tailwind CSS <https://tailwindcss.com>`_, for example, you
either create your custom components or customize components from providers,
e.g. `Tailwind UI <https://tailwindui.com>`_,
`Flowbite <https://flowbite.com>`_, or the community
`Tailwind Components <https://tailwindcomponents.com>`_.

With django CMS you make your components available to the content editors to
simply add them to a page by a click **and** frontend developers for use in templates from a single
source.

Installation
============

Install ``djangocms-frontend`` and add it to your project as described here: :ref:`built_in_components`.

If you do not use the built-in components, you do not need to add them to your ``INSTALLED_APPS``.

.. code-block:: python

    INSTALLED_APPS = [
        # Optional dependencies
        'djangocms_icon',
        'easy_thumbnails',
        'djangocms_link',  # Required if djangocms_frontend.contrib.link is used
        # Main frontend app - pre-built components not needed
        'djangocms_frontend',
    ]


Adding Styles and JavaScript
============================

When building template components, you will need to provide your custom CSS files
either by adding them to the base templates to load on every page, or by adding a
django-sekizai block to each component.

Hero component
==============

``djangocms-frontend`` allows developers to extend its functionality by creating
template components**. In this tutorial, we will create an **Hero component**
with the following fields:

- ``title``: A required text field.
- ``slogan``: A required text area field.
- ``hero_image``: A required image field.

This component will be stored in a template directory named ``<app_name>/cms_components``,
as required for ``djangocms-frontend`` template components.

Directory Structure
-------------------

The templte component lives in the template directory of any of your apps.
Ensure your DjangoCMS app has the following structure::

    theme_app/
        migrations/
        models.py
        templates/
            theme_app/
                cms_components/
                    hero.html
        views.py
        admin.py

Creating the Template Component
--------------------------------

The **template component** must be stored in the ``cms_components`` directory
inside your app. ``djangocms-frontend`` expects you to follow Django's template
namespace convention. Create a new file at::

    theme_app/templates/theme_app/cms_components/hero.html

.. note::
    No python code is required to create the component. The component is
    defined in the template itself.

Then, add the following code::

    <!-- theme_app/templates/theme_app/cms_components/hero.html -->
    {% load frontend cms_component %}

    {# Declare component - template tags are evaluated at project startup and will render empty #}
    {% cms_component "Hero" name=_("My Hero Component") %}
    {% field "title" forms.CharField required=True name=_("Title") %}
    {% field "slogan" forms.CharField required=True name=_("Slogan") widget=forms.Textarea %}
    {% field "hero_image" ImageFormField required=True name=_("Image") help_text=_("At least 1024px wide image") %}

    {# Actual template - when rendering, declared fields are available in the context #}
    <section class="bg-white dark:bg-gray-900">
        <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
            <div class="mr-auto place-self-center lg:col-span-7">
                <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white">
                    {{ title }}
                </h1>
                <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">
                    {{ slogan }}
                </p>
                    {% childplugins %}{% endchildplugins %}
            </div>
            <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
                <img src="{{ hero_image.url }}">
            </div>
        </div>
    </section>

Understanding the Code
----------------------

Component Declaration
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: django

    {% cms_component "Hero" name=_("My Hero Component") %}

This tag **declares** the component and assigns it a name (``Hero``). This is used internally
by django CMS to identify the plguin later. The ``name`` parameter is used to display the
component in the CMS admin interface. Internally the command declares a ``CMSFrontendComponent``
class. All named arguments are added to the component's Meta class.

Only one ``{% cms_component %}`` tag is allowed per template file.

The first part is the declarative part of the template:

.. code-block: django
    {% cms_component "Hero" name=_("My Hero Component") %}
    {% field "title" forms.CharField required=True name=_("Title") %}
    {% field "slogan" forms.CharField required=True name=_("Slogan") widget=forms.Textarea %}
    {% field "hero_image" ImageFormField required=True name=_("Image") help_text=_("At least 1024px wide image") %}

It will render empty. During project startup, however, these tags are evaluated and used to create the ``CMSFrontendComponent`` class
and the corresponding plugins class.

The named parameters are added to the ``CMSFrontendComponent``'s Meta class and end up as properties of the plugin itself. The
following attributes are allowed:

* ``name``: The name of the component as it will be displayed in the CMS admin interface.
* ``module``: The module the component belongs to. This is used to group components in the CMS admin interface.
* ``disable_edit``: If set to ``True``, the component will not be editable in the frontend.
* ``show_add_form``: If set to ``False``, the component will not show an add form in the frontend. This is useful if
  all component fields have valid initial values.
* ``require_parent``: If set to ``True``, the component will only be available if it is a child of another component.
* ``parent_classes``: A list of plugin classes that can be parents of this component.
* ``child_classes``: A list of plugin classes that can be children of this component.

``allow_children`` and ``frontend_editable_fields`` are set automatically.


Defining Fields
^^^^^^^^^^^^^^^

.. code-block:: django

    {% field "title" forms.CharField required=True name=_("Title") %}
    {% field "slogan" forms.CharField required=True name=_("Slogan") widget=forms.Textarea %}
    {% field "hero_image" ImageFormField required=True name=_("Image") help_text=_("At least 1024px wide image") %}

Each ``{% field %}`` tag defines a form field that content editors can use when configuring the component in the CMS.
The first parameter is the field name which is then available in the rest of the template. The second parameter is the
form field class to use. The remaining parameters are passed to the form field constructor.

By default, Django's ``django.forms`` module is available as ``forms`` in the template context. If the relevant apps are
installed, additional fields available are ``HTMLFormField`` for rich text, ``LinkFormField`` for links, and ``ImageFormField``
for images. Custom fields can be added to the context using the :attr:`~settings.DJANGOCMS_FRONTEND_COMPONENT_FIELDS` setting.

You can add additional fields to the component by adding more ``{% field %}`` tags.

Rendering the Component
^^^^^^^^^^^^^^^^^^^^^^^

After the fields are declared, the remaining part of the template is dedicated to rendering the component.
The fields declared earlier (``title``, ``slogan``, and ``hero_image``) are now available as template variables::

    <h1>{{ title }}</h1>
    <p>{{ slogan }}</p>
    <img src="{{ hero_image.url }}">

The ``{% childplugins %}`` block allows additional CMS plugins (like buttons) to be added inside the component
in the structure editor.

Make the component available in django CMS
-------------------------------------------

Template components are discovered automatically - no more coding is required. If you change the declarative
content, i.e. add/remove ``{% field %}`` tags, or change the ``{% cms_component %}`` tag, you need to restart
the Django server to apply the changes.

1. Restart your Django server.
2. Create a new page end edit it.
3. Add a new **Hero component** to a page from the plugin picker.
4. Fill in the **title**, **slogan**, and **hero image** fields.
5. Save and publish the page.

Using the component in your templates
-------------------------------------

To use the component in your templates, you can use the ``{% plugin %}`` tag with the component's name.
For example, to render the **Hero component** in a template, use the following code::

    {% load frontend %}
    {% plugin "hero" title=_("Welcome to my new website") slogan=_("Building successful websites since 1896") %}


Adding inline-editing to the component
--------------------------------------

When using `djangocms-text <https://github.com/django-cms/djangocms-text>`_, fields of the component can be
marked as inline fields to activate inline editing. Simply replace ``{{ title }}`` and/or ``{{ slogan }}`` with
``{% inline_field "title" %}`` and/or ``{% inline_field "slogan" %}``::

    <h1>{% inline_field "title" %}</h1>
    <p>{% inline_field "slogan" %}</p>

``djangocms-frontend`` will automatically register these fields with the list ``frontend_editable_fields``.

.. note::

    Django's ``runserver`` command only watches for Python source file changes. If you make changes to the
    template files, you need to restart the server manually to see the changes.


Limitations of template components
----------------------------------

Template components are a powerful tool for developers, but they have some limitations:

* **No Python code**: Template components are defined in the template itself. This means that you cannot add
  custom Python code to the component. If you need to add custom logic to a component, you should create a
  custom plugin instead. For some simple cases custom template tags also might help.
* **No custom forms**: Template components use Django forms to define the fields that content editors can use
  to configure the component. Advanced form configurations such as ``fieldsets`` are not available. If you need
  to create a custom form for a component, you should create a custom component instead.
* **Limits of the template language**: The Django template language is powerful, but it has some limitations.
  Classes are intantiated by default, for example. This is ok for ``widget=forms.Textarea``, but potentially not
  for more complex cases.

Conclusion
==========

You have successfully created a **djangocms-frontend template component** using ``cms_component``!
This structure allows editors to easily customize hero sections while maintaining a reusable
and structured design.

.. note::

    Components will create migrations since they use proxy models which are necessary, for
    example, to manage permissions. Those migrations will be added to the app containing
    the template file.
