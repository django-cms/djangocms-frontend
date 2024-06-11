.. _custom_components:

#################
Custom Components
#################

Some frontend developers prefer custom components specifically tailored to
give the project a unique and distinct look.

When working with `Tailwind CSS <https://tailwindcss.com>`_, for example, you
either create your custom components or customize components from providers,
e.g. `Tailwind UI <https://tailwindui.com>`_,
`Flowbite <https://flowbite.com>`_, or the commiunity
`Tailwind Components <https://tailwindcomponents.com>`_.

With django CMS you make your components available to the content editors for
drag and drop **and** frontend developers for use in templates from a single
source.

To use custom components in your project, add
``"djangocms_frontend.contrib.component"`` to your ``INSTALLED_APPS`` setting.

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "djangocms_frontend.contrib.component",
        ...
    ]


**djangocms-frontend** will look for custom components in the
``cms_components`` module in any of your apps. This way you can
either keep components together in one theme app, or keep them with where
they are used in different custom apps.

Let's go through this by creating a theme app::

        python manage.py startapp theme

Add a ``cms_components.py`` file to the ``theme`` app:

.. code-block:: python

    # theme/cms_components.py
    from djangocms_frontend.contrib.component.components import CMSFrontendComponent
    from djangocms_frontend.contrib.component.components import components
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
        image = ImageFormField(required=True)

        # add description for the structure board
        def get_short_description(self):
            return self.title

    @components.register
    class MyButton(CMSFrontendComponent):
        class Meta:
            name = "Button"
            render_template = "components/button.html"
            allow_children = False
            mixin = ["djangocms_frontend.contrib.link"]

        text = forms.CharField(required=True)
        link = forms.URLField(required=True)

        def get_short_description(self):
            return self.text

The template could be, for example:

.. code-block:: html

    <!-- theme/components/hero.html -->
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
                <img src="{{ instance.image_related.url }}" alt="{{ instance.image_related.alt }}">
            </div>
        </div>
    </section>
    {% addtoblock "js" %}<script src="https://cdn.tailwindcss.com"></script>{% endaddtoblock %}

As always, django CMS manages styling and JavaScript dependencies with django-sekizai.
In this example, we add the Tailwind CSS CDN to the ``js`` block.
