###############
 How-to guides
###############

.. _how to add internal link targets outside of the cms:

**************************************************
 How to add internal link targets outside the CMS
**************************************************

By default the link/button component offers available CMS pages of the
selected language as internal links.

The developer may extend this setting to include other page-generating
Django models as well by adding the ``DJANGOCMS_FRONTEND_LINK_MODELS``
setting to the project's ``.settings.py`` file.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_LINK_MODELS

    ``DJANGOCMS_FRONTEND_LINK_MODELS`` contains a list
    of additional models that can be linked.

    Each model is specified within its own dict. The resulting drop-down
    list will contain objects grouped by their type. The order of the types
    in the list is defined by the order of their definition in this setting.

    The only required attribute for each model is ``class_path``, which must
    be the full python path to the model.

    Additional attributes are:

    ``type``:
       This is the name that will appear in the grouped dropdown menu. If
       not specified, the name of the class will be used E.g., "``Page``".

    ``filter``:
       You can specify additional filtering rules here. This must be
       specified as a dict but is converted directly into kwargs internally,
       so, ``{'published': True}`` becomes ``filter(published=True)`` for
       example.

    ``order_by``:
       Specify the ordering of any found objects exactly as you would in a
       queryset. If this is not provided, the objects will be ordered in the
       natural order of your model, if any.

    ``search``:
        Specifies which (text) field of the model should be searched when
        the user types a search string.

.. note::

   Each of the defined models must define a ``get_absolute_url()``
   method on its objects or the configuration will be rejected.

Example for a configuration that allows linking CMS pages plus two
different page types from two djangocms-blog apps called "Blog" and
"Content hub" (having the ``app_config_id`` 1 and 2, respectively):

.. code::

   DJANGOCMS_FRONTEND_LINK_MODELS = [
       {
           "type": _("Blog pages"),
           "class_path": "djangocms_blog.models.Post",
           "filter": {"publish": True, "app_config_id": 1},
            "search": "translations__title",
       },
       {
           "type": _("Content hub pages"),
           "class_path": "djangocms_blog.models.Post",
           "filter": {"publish": True, "app_config_id": 2},
            "search": "translations__title",
       },
   ]

Another example might be (taken from djangocms-styledlink
documentation):

.. code::

   DJANGOCMS_FRONTEND_LINK_MODELS = [
       {
           'type': 'Clients',
           'class_path': 'myapp.Client',
           'manager_method': 'published',
           'order_by': 'title'
       },
       {
           'type': 'Projects',
           'class_path': 'myapp.Project',
           'filter': { 'approved': True },
           'order_by': 'title',
       },
       {
           'type': 'Solutions',
           'class_path': 'myapp.Solution',
           'filter': { 'published': True },
           'order_by': 'name',
       }
   ]

The link/button plugin uses select2 to show all available link targets.
This allows you to search the page titles.

.. warning::

   If you have a huge number (> 1,000) of link target (i.e., pages or
   blog entries or whatever) the current implementation might slow down
   the editing process. In your ``settings`` file you can set
   ``DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH`` to a value greater than 1 and
   **djangocms-frontend** will wait until the user inputs at least this many
   characters before querying potential link targets.

********************************
 How to extend existing plugins
********************************

Existing plugins can be extended through two type of class mixins.
``djangocms-frontend`` looks for these mixins in two places:

#. In the theme module. Its name is specified by the setting
   ``DJANGOCMS_FRONTEND_THEME`` and defaults to ``djangocms_frontend``.
   For a theme app called ``theme`` and the bootstrap5 framework this
   would be ``theme.frontends.bootstrap5.py``.

#. In djangocms_frontend.contrib.*app*.frontends.*framework*.py. For the
   alert app and the bootstrap5 framework this would be
   ``djangocms_frontend.contrib.alert.frontends.bootstrap5.py``.

Both mixins are included if they exist and all methods have to call the
super methods to ensure all form extensions and render functionalities
are processed.

The theme module is primarily thought to allow for third party
extensions in terms of functionality and/or design.

The framework module is primarily thought to allow for adaptation of
``djangocms-frontend`` to other css frameworks besides Bootstrap 5.

RenderMixins
============

The render mixins are called "*PluginName*RenderMixin", e.g.
``AlertRenderMixin`` and are applied to the plugin class. This allows
for the redefinition of the ``CMSPlugin.render`` method, especially to
prepare the context for rendering.

Also it can add fields to the front end editiong form by subclassing
``CMSPlugin.get_fieldsets``. This allows for extension or change of the
plugin's admin form. The admin form is used to edit or create a plugin.

FormMixins
==========

Form mixins are used to add fields to a plugin's admin form. These
fields are available to the render mixins and, of course, to the plugin
templates.

Form mixins are calle "*PluginName*FormMixin", e.g. ``AlertFormMixin`` and are
applied to the editing form class. Form mixins are a subclass of
``entangled.EntangeldModelFormMixin``.


Working example
===============

Let's say you wanted to extend the ``GridContainerPlugin`` to offer the
option for a background image, and say a blur effect.

First, you add some fields to the ``GridContainerForm`` (in
*theme*.forms):

.. code:: forms.py

    from django import forms
    from django.db.models import ManyToOneRel
    from django.utils.translation import gettext as _
    from djangocms_frontend import settings
    from entangled.forms import EntangledModelFormMixin
    from filer.fields.image import AdminImageFormField, FilerImageField
    from filer.models import Image


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
            choices=settings.EMPTY_CHOICE + settings.IMAGE_POSITIONING,
            initial="",
            label=_("Background image position"),
        )
        container_blur = forms.IntegerField(
            required=False,
            initial=0,
            min_value=0,
            max_value=10,
            #       widget=forms.TextInput(attrs=dict(type="range", min=0, max=10)),
            help_text=_("Blur of container image (in px)."),
        )

Then, add a ``GridContainerMixin`` in ``*theme*.bootstrap5.py``:

.. code:: bootstrap5.py

    from django.utils.translation import gettext as _
    from djangocms_frontend.helpers import insert_fields


    class GridContainerRenderMixin:
        render_template = "djangocms_frontend/bootstrap5/grid_container.html"

        def get_fieldsets(self, request, obj=None):
            return insert_fields(
                super().get_fieldsets(request, obj),
                (
                    "container_image",
                    (
                        "image_position",
                        "container_blur",
                    ),
                ),
                block=None,
                position=1,
                blockname=_("Image"),
            )

        def render(self, context, instance, placeholder):
            if getattr(instance, "container_image", None):
                instance.add_classes("imagecontainer")
                context["bg_color"] = (
                    f"bg-{instance.container_context}"
                    if getattr(instance, "container_context", False)
                    else ""
                )
            elif getattr(instance, "container_context", False):
                instance.add_classes(f"bg-{instance.container_context}")
                if getattr(instance, "container_opacity", "100") != "100":
                    instance.add_classes(f"bg-opacity-{instance.container_opacity}")
                context["bg_color"] = False
            return super().render(context, instance, placeholder)


The ``render`` method provides required context data for the extended
functionality. In this case it adds "imagecontainer" to the list of
classes for the container, processes the background colors, as well as
opacity and blur.

The ``get_fieldsets`` methed is used to make Django-CMS show the new
form fields in the plugin's edit modal (admin form, technically
speaking).

Lastly, a new template is needed (in
``"djangocms_frontend/bootstrap5/grid_container.html"``):

.. code:: grid_container.html

    {% load cms_tags %}{% spaceless %}
        <{{ instance.tag_type }}{{ instance.get_attributes }}
            {% if instance.container_opacity and not instance.image %}
                style="opacity: {{ instance.container_opacity }}%;
                       {% if instance.container_blur %}
                          backdrop-filter: blur({{ instance.container_blur }}px);
                       {% endif %}"
            {% endif %}
        >
          {% if instance.image %}
            <div class="image"
                style="background-image: url('{{ instance.image.url }}');
                       background-position: {{ instance.image_position|default:'center center' }};
                       background-repeat: no-repeat;
                       background-size: cover;
                       {% if instance.container_blur %}
                         filter: blur({{instance.container_blur}}px);
                       {% endif %}">
            </div>
          {% elif instance.container_image %}
            <div class="image placeholder placeholder-wave"></div>
          {% endif %}
          {% if bg_color %}
            <div class="cover {{bg_color}}"{% if instance.container_opacity %}
                 style="opacity: {{ instance.container_opacity }}%"{% endif %}>
            </div>
          {% endif %}
          {% if "imagecontainer" in add_classes %}<div class="content">{% endif %}
            {% for plugin in instance.child_plugin_instances %}
                {% render_plugin plugin %}
            {% endfor %}
          {% if "imagecontainer" in add_classes %}</div>{% endif %}
        </{{ instance.tag_type }}>
    {% endspaceless %}

With these three additions, all grid container plugins will now have
additional fields to define abckground images to cover the container
area.

If the theme is taken out of the path djangocms-frontend will fall back
to its basic functionality, i.e. the background images will not be
shown. As long as plugins are not edited the background image
information will be preserved.

***************************
 How to create a theme app
***************************

``djangocms-frontend`` is designed to be "themable". A theme typically
will do one or more of the following:

-  Style the appearance using css
-  Extend standard plugins
-  Add custom plugins

******************************************************
 How to add the tab editing style to my other plugins
******************************************************

If you prefer the tabbed frontend editing style of **djangocms-frontend** you
can easily add it to your own plugins.

If you use the standard editing form, just add a line specifying the
``change_form_template`` to your plugin class:

.. code-block::

    class MyCoolPlugin(CMSPluginBase):
        ...
        change_form_template = "djangocms_frontend/admin/base.html"
        ...


If you already have your own ``change_form_template``, make sure it extends
``djangocms_frontend/admin/base.html``:

.. code-block::

    {% extends "djangocms_frontend/admin/base.html" %}
    {% block ...%}
        ...
    {% endblock %}
