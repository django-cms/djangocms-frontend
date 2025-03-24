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

Custom components are part of the djangocms-frontend root package and do not
require additional listing in the ``INSTALLED_APPS`` setting.

djangocms-frontend allows developers to extend its functionality by creating
template components**. In this tutorial, we will create an **Hero component**
with the following fields:

- ``title``: A required text field.
- ``slogan``: A required text area field.
- ``hero_image``: A required image field.

This component will be stored in a template directory named ``<app_name>/cms_components``,
as required for djangocms-frontend template components.

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
inside your app. djangocms-frontend expects you to follow Django's template
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

::

    {% cms_component "Hero" name=_("My Hero Component") %}

This tag **declares** the component and assigns it a name (``Hero``). This is used internally
by django CMS to identify the plguin later. The ``name`` parameter is used to display the
component in the CMS admin interface. Internally the command declares a ``CMSFrontendComponent``
class. All named arguments are added to the component's Meta class.

Defining Fields
^^^^^^^^^^^^^^^

::

    {% field "title" forms.CharField required=True name=_("Title") %}
    {% field "slogan" forms.CharField required=True name=_("Slogan") widget=forms.Textarea %}
    {% field "hero_image" ImageFormField required=True name=_("Image") help_text=_("At least 1024px wide image") %}

Each ``{% field %}`` tag defines a form field that content editors can use when configuring the component in the CMS.
The first parameter is the field name which is then available in the rest of the template. The second parameter is the
form field class to use. The remaining parameters are passed to the form field constructor.

By default, Django's ``django.forms`` module is available as ``forms`` in the template context. If the relevant apps are
installed, additional fields available are ``HTMLFormField`` for rich text, ``LinkFormField`` for links, and ``ImageFormField``
for images.

Rendering the Component
^^^^^^^^^^^^^^^^^^^^^^^

After the fields are declared, the remaining part of the template is dedicated to rendering the component.
The fields declared earlier (``title``, ``slogan``, and ``hero_image``) are now available as template variables::

    <h1>{{ title }}</h1>
    <p>{{ slogan }}</p>
    <img src="{{ hero_image.url }}">

The ``{% childplugins %}`` block allows additional CMS plugins (like buttons) to be added inside the component
in the structure editor.

Make the component avialabvle in django CMS
-------------------------------------------

Template components are discovered automatically - no more coding is required. If you change the declarative
content, i.e. add/remove ``{% field %}`` tags, or change the ``{% cms_component %}`` tag, you need to restart
the Django server to apply the changes.

1. Restart your Django server.
2. Create a new page end edit it.
3. Add a new **Hero component** to a page from the plugin picker.
4. Fill in the **title**, **slogan**, and **hero image** fields.
5. Save and publish the page.

Conclusion
----------

You have successfully created a **djangocms-frontend template component** using ``cms_component``!
This structure allows editors to easily customize hero sections while maintaining a reusable
and structured design.

