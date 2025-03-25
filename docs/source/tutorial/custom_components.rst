.. _custom_components:

##########################
Building custom frontend components
##########################

.. index::
    single: custom frontend components

.. versionadded:: 2.0

custom frontend components are a powerful tool for content editors, allowing them to build pages without needing
in-depth knowledge of design, HTML, or nested structures. Editors can simply add content to pre-defined
components, creating visually cohesive pages with ease.

When working with `Tailwind CSS <https://tailwindcss.com>`_, for example, you
either create your custom frontend components or customize components from providers,
e.g. `Tailwind UI <https://tailwindui.com>`_,
`Flowbite <https://flowbite.com>`_, or the community
`Tailwind Components <https://tailwindcomponents.com>`_.

With django CMS you make your components available to the content editors to simply add them to a page by a
click **and** frontend developers for use in templates from a single source.

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

Hero component example
======================

``djangocms-frontend`` will look for custom frontend components in the
**``cms_components`` module in any of your apps**. This way you can
either keep components together in one theme app, or keep them with where
they are used in different custom apps.

Directory Structure
-------------------

Let's go through this by creating a theme app::

        python manage.py startapp theme

Custom frontend components live in the ``cms_components`` module of any of your apps.
Ensure your app has the following structure::

    theme/
        cms_components.py
        migrations/
        models.py
        templates/
            components/
                hero.html
        views.py
        admin.py

Creating two Custom Frontend Components
---------------------------------------

Add a ``cms_components.py`` file to the ``theme`` app (see structure above):

.. code-block:: python

    # theme/cms_components.py
    from djangocms_link.fields import LinkFormField

    from djangocms_frontend.component_base import CMSFrontendComponent
    from djangocms_frontend.component_pool import components
    from djangocms_frontend.contrib.image.fields import ImageFormField


    @components.register
    class MyHeroComponent(CMSFrontendComponent):
        class Meta:
            # declare plugin properties
            name = "My Hero Component"
            render_template = "components/hero.html"
            allow_children = True
            mixins = ["Background"]
            # for more complex components, you can add fieldsets

        # declare fields
        title = forms.CharField(required=True)
        slogan = forms.CharField(required=True, widget=forms.Textarea)
        hero_image = ImageFormField(required=True)

        # add description for the structure board
        def get_short_description(self):
            return self.title

    @components.register
    class MyButton(CMSFrontendComponent):
        class Meta:
            name = "Button"
            render_template = "components/button.html"
            allow_children = False

        text = forms.CharField(required=True)
        link = LinkFormField()

        def get_short_description(self):
            return self.text

The templates could be, for example:

.. code-block:: django

    <!-- theme/templates/components/hero.html -->
    {% load cms_tags frontend sekizai_tags %}
    <section class="bg-white dark:bg-gray-900">
        <div class="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-8 xl:gap-0 lg:py-16 lg:grid-cols-12">
            <div class="mr-auto place-self-center lg:col-span-7">
                <h1 class="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white">
                    {{ instance.title }}
                </h1>
                <p class="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400">
                    {{ instance.message }}
                </p>
                    {% childplugins instance %}
                        <a href="#" class="inline-flex items-center justify-center px-5 py-3 mr-3 text-base font-medium text-center text-white rounded-lg bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:focus:ring-primary-900">
                            Get started
                            <svg class="w-5 h-5 ml-2 -mr-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                        </a>
                        <a href="#" class="inline-flex items-center justify-center px-5 py-3 text-base font-medium text-center text-gray-900 border border-gray-300 rounded-lg hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800">
                             Speak to Sales
                         </a>
                     {% endchildplugins %}
            </div>
            <div class="hidden lg:mt-0 lg:col-span-5 lg:flex">
                <img src="{{ instance.hero_image.url }}" alt="{{ instance.image_related.alt }}">
            </div>
        </div>
    </section>
    {% addtoblock "js" %}<script src="https://cdn.tailwindcss.com"></script>{% endaddtoblock %}


.. code-block:: django

    <!-- theme/templates/components/button.html -->
    {% load djangocms_link_tags %}

    <a class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
       href="{{ instance.link|to_url }}">{{ instance.text }}</a>

As always, django CMS manages styling and JavaScript dependencies with django-sekizai.
In this example, we add the Tailwind CSS CDN to the ``js`` block.

Understanding the Code
----------------------



Limitations of custom frontend components
=========================================

Custom frontend components are a powerful tool for developers, but they have a limitations:

**Limited Python code**: Custom components are (indirect) subclasses of Django's ``AdminForm`` class
and can contain Python code to modify the behavior of a form. You cannot directly add Python code to
the resulting plugin class with the exception of ``get_render_template()`` and ``save_model()``.
Similarly, you cannot add Python code the model class, in this case with the exception of ``get_short_description()``.

Conclusion
==========

In this tutorial, we explored how to create custom frontend components. These components empower developers to
provide visually appealing components to content editors with minimal coding.

By following the steps outlined above, you can:

- Create a theme app to house your custom components.
- Define components using the `CMSFrontendComponent` class.
- Leverage templates to control the visual presentation of your components.
- Register and manage your components seamlessly within django CMS.

.. note::

    Components will create migrations since they use proxy models which are necessary, for
    example, to manage permissions. Those migrations will be added to the app containing
    the ``cms_component.py`` file.
