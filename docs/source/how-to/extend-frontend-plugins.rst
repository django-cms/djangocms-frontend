.. _how-to-extend-frontend-plugins:

**********************************
 How to extend built-in components
**********************************

Existing components can be extended through **two type of class mixins**.
``djangocms-frontend`` tries to autodiscover them by looking for these mixins
in two places:

#. In a custom theme app. Its name is specified by the setting
   ``DJANGOCMS_FRONTEND_THEME`` and defaults to ``theme``.
   For a theme app called ``theme`` and the bootstrap5 framework djangocms-frontend
   would look for the class mixins in ``theme.frameworks.bootstrap5.py``.

   .. note::

      Make sure to include your custom theme app in your project setting's ``INSTALLED_APPS``,
      plus pointed to by the ``DJANGOCMS_FRONTEND_THEME`` setting::

         INSTALLED_APPS = [
             ...,
             'theme',  # Needs to be included to make custom theme templates available
             ...
         ]
         DJANGOCMS_FRONTEND_THEME = "theme"  # Change if necessary


#. In ``djangocms_frontend.contrib.<app>.frontends.<framework>.py``. For the
   alert app and the bootstrap5 framework this would be
   ``djangocms_frontend.contrib.alert.frontends.bootstrap5.py``. These are the
   standard mixins for standard components.

Both mixins are included if they exist and all methods have to call the
super methods to ensure all form extensions and render functionalities
are processed.

The theme module is primarily thought to allow for third party
extensions in terms of functionality and/or design.

The framework module is primarily thought to allow for adaptation of
``djangocms-frontend`` to other css frameworks besides Bootstrap 5.

.. index::
    single: RenderMixins

RenderMixins
============

The render mixins are called ``<PluginName>RenderMixin``, e.g.
``AlertRenderMixin`` and are applied to the plugin class. This allows
for the redefinition of the ``CMSPlugin.render`` method, especially to
prepare the context for rendering.

Also it can add fields to the front end editing form by subclassing
``CMSPlugin.get_fieldsets``. This allows for extension or change of the
plugin's admin form. The admin form is used to edit or create a plugin.

.. index::
    single: FormMixins

FormMixins
==========

Form mixins are used to add fields to a plugin's admin form. These
fields are available to the render mixins and, of course, to the plugin
templates.

Form mixins are called ``<PluginName>FormMixin``, e.g. ``AlertFormMixin`` and are
applied to the editing form class. Form mixins are a subclass of
``entangled.EntangledModelFormMixin``.

.. index::
    single: Working example

.. index::
    single: Create a theme
    single: Themes

Working example: Extending the ``GridContainerPlugin``
======================================================

Let's say you wanted to extend the ``GridContainerPlugin`` to offer the
option for a background image, and say a blur effect. The way to do it
is to create a theme app. You are free to chose its name. For this example
we take it to be "theme". Please replace "theme" by your own theme's name.

First, create a directory structure like this:

.. code-block::

    theme
    ├── __init__.py
    ├── forms.py
    ├── frameworks
    │   ├── __init__.py
    │   └── bootstrap5.py
    ├── static
    │   └── css
    │       └── background_image.css
    └── templates
        └── djangocms_frontend
            └── bootstrap5
                └── grid_container.html


All ``__init__.py`` files remain empty.

Next, you add some fields to the ``GridContainerForm`` (in
``theme/forms.py``):

.. code:: python

    from django import forms
    from django.db.models import ManyToOneRel
    from django.utils.translation import gettext as _
    from djangocms_frontend import settings
    from entangled.forms import EntangledModelFormMixin
    from filer.fields.image import AdminImageFormField, FilerImageField
    from filer.models import Image


    IMAGE_POSITIONING = (
        ("center center", _("Fully Centered")),
        ("left top", _("Top left")),
        ("center top", _("Top center")),
        ("right top", _("Top right")),
        ("left center", _("Center left")),
        ("right center", _("Center right")),
        ("left bottom", _("Bottom left")),
        ("center bottom", _("Bottom center")),
        ("right bottom", _("Bottom right")),
    )


    class GridContainerFormMixin(EntangledModelFormMixin):
        class Meta:
            entangled_fields = {
                "config": [
                    "container_image",
                    "image_position",
                    "container_blur",
                ]
            }

        container_image = AdminImageFormField(
            rel=ManyToOneRel(FilerImageField, Image, "id"),
            queryset=Image.objects.all(),
            to_field_name="id",
            label=_("Image"),
            required=False,
            help_text=_("If provided used as a cover for container."),
        )
        image_position = forms.ChoiceField(
            required=False,
            choices=settings.EMPTY_CHOICE + IMAGE_POSITIONING,
            initial="",
            label=_("Background image position"),
        )
        container_blur = forms.IntegerField(
            required=False,
            initial=0,
            min_value=0,
            max_value=10,
            help_text=_("Blur of container image (in px)."),
        )

.. warning::

    These form fields are mixed to the original form. Please make sure to
    avoid name collisions for the fields.

.. note::

    If you need to add many form mixins, consider turning ``forms.py`` into a
    package, i.e. create a directory ``forms`` and distribute the mixins over
    several files, e.g., ``forms/marketing_forms.py`` etc., and importing the
    all mixins relevant to ``djangocms-frontend`` into the directory's
    ``__init__.py``.

Rendering should be done with the Bootstrap 5 framework. Hence all rendering
mixins go into ``theme/bootstrap5.py``. Since we are extending the
``GridContainer`` plugin the appropriate mixin to define is
``GridContainerMixin``:

.. code:: python

    from django.utils.translation import gettext as _
    from djangocms_frontend.helpers import insert_fields


    class GridContainerRenderMixin:
        render_template = "djangocms_frontend/bootstrap5/grid_container.html"

        def get_fieldsets(self, request, obj=None):
            """Extend the fieldset of the plugin to contain the new fields
            defined in forms.py"""
            return insert_fields(
                super().get_fieldsets(request, obj),
                (
                    "container_image",
                    (
                        "image_position",
                        "container_blur",
                    ),
                ),
                block=None,  # Create a new fieldset (called block here)
                position=1,  # at position 1 (i.e. directly after the mail fieldset)
                blockname=_("Image"),  # and call the fieldset "Image"
            )

        def render(self, context, instance, placeholder):
            """Render should process the form fields and turn them into appropriate
            context items or add corresponding classes to the instance"""
            if getattr(instance, "container_image", None):
                instance.add_classes("imagecontainer")
                context["bg_color"] = (
                    f"bg-{instance.background_context}"
                    if getattr(instance, "background_context", False)
                    else ""
                )
            return super().render(context, instance, placeholder)

.. warning::

    Do not forget to call ``super()`` in both the ``get_fieldsets`` and the
    ``render`` method.


The ``render`` method provides required context data for the extended
functionality. In this case it adds ``imagecontainer`` to the list of
classes for the container, processes the background colors since it should
appear above the image (and not below), as well as blur.

The ``get_fieldsets`` method is used to make django CMS show the new
form fields in the plugin's edit modal (admin form, technically
speaking).

Then, a new template is needed (in
``theme/templates/djangocms_frontend/bootstrap5/grid_container.html``):

.. code::

    {% load cms_tags sekizai_tags static %}{% spaceless %}
      <{{ instance.tag_type }}{{ instance.get_attributes }}
      {% if instance.background_opacity and not instance.image %}
        {% if instance.container_blur %}
          backdrop-filter: blur({{ instance.container_blur }}px);
        {% endif %}"
      {% endif %}>
      {% if instance.container_image %}
        <div class="image"
          style="background-image: url('{{ instance.container_image.url }}');
                 background-position: {{ instance.image_position|default:'center center' }};
                 background-repeat: no-repeat;background-size: cover;
                 {% if instance.container_blur %}
                   filter: blur({{ instance.container_blur }}px);
                 {% endif %}">
        </div>
      {% elif instance.container_image %}
        <div class="image placeholder placeholder-wave"></div>
      {% endif %}
      {% if bg_color %}
        <div class="cover {{ bg_color }}"{% if instance.background_opacity %}
             style="opacity: {{ instance.background_opacity }}%"{% endif %}></div>
      {% endif %}
      {% if instance.container_image %}
        <div class="content">
      {% endif %}
        {% for plugin in instance.child_plugin_instances %}
          {% render_plugin plugin %}
        {% endfor %}
      {% if instance.container_image %}</div>{% endif %}
    </{{ instance.tag_type }}>{% endspaceless %}
    {# Only add if the css is not included in your site's global css #}
    {% addtoblock 'css' %}
        <link rel="stylesheet" href="{% static 'css/background_image.css' %}">
    {% endaddtoblock %}


Finally, a set of css style complement the new template. The styles can either
be added to the css block in the template (if used scarcely and as done in
the above example) or directly to your project's css files.

The required styles are:

.. code::

    /* Image Container */

    div.imagecontainer {
        position: relative;
        min-height: 112px;
    }

    div.imagecontainer > div.cover,
    div.imagecontainer > div.image {
        position: absolute;
        left:0;
        right:0;
        top:0;
        bottom:0;
    }

    div.imagecontainer > div.content {
        position: relative;
    }


With these three additions, all grid container plugins will now have
additional fields to define background images to cover the container
area.

If the theme is taken out of the path ``djangocms-frontend`` will fall back
to its basic functionality, i.e. the background images will not be
shown. As long as plugins are not edited the background image
information will be preserved.

.. note::

    A few suggestions on extending ``djangocms-frontend``:

    *   You may think of customizing bootstrap by including a folder ``sass`` in
        your theme app. For more see `Bootstrap 5 documentation on customizing
        <https://getbootstrap.com/docs/5.1/customize/overview/>`_.

    *   If you need entirely new plugins, create a file ``cms_plugins.py`` and
        import ``CMSUIPlugin`` (import from ``djangocms_frontend.cms_plugins``)
        as base class for the plugins.

    *   Create ``models.py`` file for the models (which need to be proxy models
        of ``FrontendUIItem`` (import from ``djangocms_frontend.models``).
