.. _template_components:

############################
Simplified Component Creation with Templates
############################

.. index::
    single: Template Components
    single: Auto Components

.. versionadded:: 2.1

**Template components** are the easiest approach to creating or porting your own custom
frontend components, allowing you to define custom components **using Django templates,
without needing to write any Python code**.


Example Hero Template Component
===============================

In this tutorial, we will create a **Hero template component** with the following fields:

- ``title``: A required text field.
- ``slogan``: A required text area field.
- ``hero_image``: A required image field.

This component will be declared by using special djangocms tags in a template file,
with no python code required.

Directory Structure
-------------------

`djangocms-frontend` will **automatically locate and register template components** by looking for them
 in the **``templates/<app_name>/cms_components/``** directory of your installed apps.

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

In this example, ``theme_app/templates/theme_app/cms_components/hero.html`` will be the template
defining our custom hero component.

.. note::
    You can change the location of your template components inside your template directory
    by setting the :attr:`DJANGOCMS_FRONTEND_COMPONENT_FOLDER` setting. The default is
    ``cms_components``. If you change it, you need to adjust the directory structure accordingly.


Creating the Template Component
--------------------------------

Add the following code to the `hero.html` template::

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
                {# Get the related object of the image field which itself is just a dict #}
                {% with image=instance.hero_image|get_related_object %}
                    <img src="{{ image.url }}" alt="{{ image.alt }}">
                {% endwith %}
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
by django CMS to identify the plugin later. The ``name`` parameter is used to display the
component in the CMS admin interface. Internally the command declares a ``CMSFrontendComponent``
class. All named arguments are added to the component's Meta class.

.. note::
    The component name (the first argument to ``{% cms_component %}``) must be a valid Python identifier.
    This means it should start with a letter or underscore, followed by letters, digits, or underscores,
    and cannot contain spaces or special characters like hyphens.

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
in the structure editor. Anything in between ``{% childplugins %}`` and ``{% endchildplugins %}`` will only be
rendered if the component has no children.


Make the component available in django CMS
-------------------------------------------

Template components are discovered automatically - no more coding is required. If you change the declarative
content, i.e. add/remove ``{% field %}`` tags, or change the ``{% cms_component %}`` tag, you need to restart
the Django server to apply the changes.

1. Restart your Django server.
2. Create a new page And edit it.
3. Add a new **Hero component** to a page from the plugin picker.
4. Fill in the **title**, **slogan**, and **hero image** fields.
5. Save and publish the page.

Using the component in your templates
-------------------------------------

To use the component in your templates outside django CMS, you can use the ``{% plugin %}`` tag with the
component's name. For example, to render the **Hero component** in a template, use the following code::

    {% load frontend %}
    {% plugin "hero" title=_("Welcome to my new website") slogan=_("Building successful websites since 1896") %}

.. note::
    Do not forget to register the component with :attr:`CMS_COMPONENT_PLUGINS`. If you needed to list the single
    component in the setting, the hero component's dotted path to its plugin would be
    ``djangocms_frontend.cms_plugins.HeroPlugin``.


Adding inline-editing to the component
--------------------------------------

When using `djangocms-text <https://github.com/django-cms/djangocms-text>`_, `CharField` and `HTMLFormField` fields
of the component can be marked as inline fields to activate inline editing. Inline-editing fields can be changed in
the edit endpoint by simply clicking inside and typing over the text - without the need to open an edit dialogue for
the component.

Simply replace ``{{ title }}`` and/or ``{{ slogan }}`` with ``{% inline_field "title" %}`` and/or
``{% inline_field "slogan" %}``::

    <h1>{% inline_field "title" %}</h1>
    <p>{% inline_field "slogan" %}</p>

``djangocms-frontend`` will automatically register these fields with the list ``frontend_editable_fields``.

.. note::

    Django's ``runserver`` command only watches for Python source file changes. If you make changes to the
    template files, you need to restart the server manually to see the changes.


A little helper: the ``split`` filter
-------------------------------------

.. index::
    single: split filter
    single: choices in template components

If you load the ``cms_component`` template tag library, you can use the ``split`` filter to convert a string into a list.
Some component properties require a list of values, such as the ``parent_classes`` or ``child_classes``.
You can use the ``split`` filter to convert a string into a list. For example, if you want to allow the
**Hero component** to be a child of the **Container or Column component**, you can set the ``parent_classes``
like this::

    {% cms_component "Hero" name=_("My Hero Component") parent_classes="ContainerPlugin|ColumnPlugin"|split %}

``split`` splits a string by the pipe character (``|``) and returns a list of strings. If you prefer to use a different
separator, you can pass it as an argument to the filter, like this::

    {% cms_component "Hero" name=_("My Hero Component") parent_classes="ContainerPlugin,ColumnPlugin"|split:"," %}

Additionally, ``split`` can be used to create tuples as needed for the ``choices`` parameter of
``forms.ChoiceField``. For example, if you want to create a choice field with two options, you can use the
following code::

    {% field "color" forms.ChoiceField choices=_("Red <red>|Green <green>|Default <blue>")|split name=_("Color") %}

The verbose choice label is appended by the actual value of the field between angle brackets (``<...>``).

.. note::

    For translators it is important to know, that they **should not translate** the value in angle brackets.
    The German translation of the above example string might be ``Rot <red>|Grün <green>|Standard <blue>``.


Limitations of template components
==================================

Template components are a powerful tool for developers, but they have some limitations:

* **No Python code**: Template components are defined in the template itself. This means that you cannot add
  custom Python code to the component. If you need to add custom logic to a component, you should create a
  custom plugin instead. For some simple cases custom template tags also might help.
* **No custom forms**: Template components use Django forms to define the fields that content editors can use
  to configure the component. Advanced form configurations such as ``fieldsets`` are not available. If you need
  to create a custom form for a component, you should create a custom component instead.
* **Limits of the template language**: The Django template language is powerful, but it has some limitations.
  Classes are instantiated by default, for example. This is ok for ``widget=forms.Textarea``, but potentially not
  for more complex cases.

For more powerful customization options, consider building a :ref:`custom Frontend Component <custom_components>`
or a :ref:`custom Plugin<how-to-add-frontend-plugins>`


Examples
========

The djangocms-frontend repository contains a small number of example components in the
`examples directory <https://github.com/django-cms/djangocms-frontend/tree/master/examples>`_.
They are taken from the `Bootstrap 5 examle page <https://getbootstrap.com/docs/5.3/examples/>`_
and modified to include the template component tags.

Examples are not installed through the package. You can copy them to your project and adapt them
to your needs.

Troubleshooting
================

If the component does not appear in the plugin picker, check the following:

1. **INSTALLED_APPS**: Verify that the app containing the component is listed in your ``INSTALLED_APPS`` setting.

2. **Template Location**: Ensure the template file is located in the correct directory structure:
   ``templates/<app_name>/cms_components/`` inside your app.

3. **Server Restart**: Restart the Django server after creating or modifying the component template. Changes in
   the declarative part are only reflected after server restart.

4. **Rendering exceptions**: The template component will only be added if it renders without exception. Make
   sure it does not fail if the context is empty. Check the server logs for errors during startup. Missing
   dependencies or syntax errors in the template can prevent the component from being registered.

5. **Migration module**: Make sure the app has a migration module. If not, create one with
   ``python -m manage makemigrations <app_name>``.

6. **Permissions**: Add the necessary permissions for the user/group if you are not the superuser.
   Also see :ref:`sync_permissions`.

If the issue persists, double-check the template syntax and ensure all required fields are properly defined.

Conclusion
==========

In this tutorial, you learned how to create a reusable **Hero component** using ``djangocms-frontend``.
This approach allows you to:

- Simplify component creation for editors by offering inline editing.
- Maintain consistent design across your website by reusing the component.
- Extend functionality without writing Python code.

By following these steps, you can create additional components tailored to your project's needs.


.. note::

    Components will create migrations since they use proxy models which are necessary, for
    example, to manage permissions. Those migrations will be added to the app containing
    the template file.
