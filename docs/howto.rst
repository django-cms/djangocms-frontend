How-to guides
#############

How to extend existing plugins
******************************

Existing plugins can be extended through two type of
class mixins. ``djangocms-frontend`` looks for these mixins
in two places:

1. In the theme module. Its name is specified by the setting
   ``DJANGOCMS_FRONTEND_THEME`` and defaults to ``djangocms_frontend``. For a
   theme app called ``theme`` and the bootstrap5 framework this would
   be ``theme.frontends.bootstrap5.py``.

2. In djangocms_frontend.contrib.*app*.frontends.*framework*.py. For the alert
   app and the bootstrap5 framework this would be
   ``djangocms_frontend.contrib.alert.frontends.bootstrap5.py``.

Both mixins are included if they exist and all methods have to call the super methods
to ensure all form extensions and render functionalities are processed.

The theme module is primarily thought to allow for third party
extensions in terms of functionality and/or design.

The framework module is primarily thought to allow for adaptation of
``djangocms-frontend`` to other css frameworks besides Bootstrap 5.


RenderMixins
============

The render mixins are called "*PluginName*RenderMixin", e.g. ``AlertRenderMixin``
and are applied to the plugin class. This allows for the redefinition of
the ``CMSPlugin.render`` method, especially to prepare the context for rendering.

In addition it allows the definition of ``CMSPlugin.get_fieldsets`` it
allows for extension or change of the plugin's admin form. The admin form
is used to edit or create a plugin.

FormMixins
==========

Form mixins are used to add fields to a plugin's admin form.
These fields are available to the render mixins and, of course,
to the plugin templates.

Working example
===============

Let's say you wanted to extend the ``GridContainerPlugin`` to
offer the option for a background color, a background image,
some transparency and say a blur effect.

First, you add some fields to the ``GridContainerForm`` (in *theme*.forms): ::


    from django.db.models import ManyToOneRel
    from django import forms
    from django.utils.translation import gettext as _
    from djangocms_frontend.fields import ColoredButtonGroup
    from filer.fields.image import AdminImageFormField, FilerImageField
    from filer.models import Image

    from djangocms_frontend import settings
    from entangled.forms import EntangledModelFormMixin

    class GridContainerFormMixin(EntangledModelFormMixin):
        class Meta:
            entangled_fields = {
                "config": [
                    "container_context",
                    "container_opacity",
                    "container_image",
                    "image_position",
                    "container_blur",
                ]
            }

        container_context = forms.ChoiceField(
            label=_("Background context"),
            required=False,
            choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
            initial=settings.EMPTY_CHOICE,
            help_text=_("Covers image."),
            widget=ColoredButtonGroup(),
        )
        container_opacity = forms.IntegerField(
            label=_(""),
            required=False,
            initial=100,
            widget=forms.TextInput(attrs=dict(type="range", min=0, max=100)),
            help_text=_("Opacity of container background (left: transparent, right: opaque).")
        )
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



Then, add a ``GridContainerMixin`` in *theme*.bootstrap5: ::

    from django.utils.translation import gettext as _
    from djangocms_frontend.helpers import insert_fields


    class GridContainerRenderMixin:
        def render(self, context, instance, placeholder):
            if getattr(instance, "container_image", None):
                context["add_classes"] = "imagecontainer"
                context["bg_color"] = f"bg-{instance.container_context}" if getattr(instance, "container_context", False) else ""
            else:
                context["add_classes"] = f"bg-{instance.container_context}" if getattr(instance, "container_context", False) else ""
                context["bg_color"] = False
            return super().render(context, instance, placeholder)

        def get_fieldsets(self, request, obj=None):
            return insert_fields(self.fieldsets, (
                        "container_context",
                        "container_image",
                        ("image_position", "container_opacity", ),
                    ), block=None, position=1, blockname=_("Background"))

The ``render`` method provides required context data for the extended functionality.
In this case it adds "imagecontainer" to the list of classes for the container, processes
the background colors, as well as opacity and blur.

The ``get_fieldsets`` methed is used to make Django-CMS show the new form fields in
the plugin's edit modal (admin form, technically speaking).

Lastly, a new template is needed (in
``"djangocms_frontend/bootstrap5/grid_container.html"``): ::

    {% load cms_tags frontend %}{% spaceless %}
        <{{ instance.tag_type }} {% add_class instance.attributes instance.container_type add_classes %}
            {% if instance.container_opacity and not instance.image %}style="opacity: {{ instance.container_opacity }}%;" {% endif %}
        >
          {% if instance.image %}
            <div class="image"
            style="background-image: url('{{ instance.image.url }}');
                   background-position: {{ instance.image_position|default:'center center' }};
                   background-repeat: no-repeat;background-size: cover;">
            </div>
          {% elif instance.container_image %}
            <div class="image placeholder placeholder-wave"></div>
          {% endif %}
          {% if bg_color %}
            <div class="cover {{bg_color}}"{% if instance.container_opacity %} style="opacity: {{ instance.container_opacity }}%"{% endif %}></div>
          {% endif %}
          {% if "imagecontainer" in add_classes %}<div class="content">{% endif %}
            {% for plugin in instance.child_plugin_instances %}
                {% render_plugin plugin %}
            {% endfor %}
          {% if "imagecontainer" in add_classes %}</div>>{% endif %}
        </{{ instance.tag_type }}>{% endspaceless %}

With these three additions, all grid container plugins will now have additional
fields to define abckground images to cover the container area.

If the theme is taken from the path djangocms-frontend will fall back to its
basic functionality, i.e. the background images will not be shown. As long as
plugins are not edited the background image information will be preserved.

How to create a theme app
*************************
``djangocms-frontend`` is designed to be "themable".
A theme typically will do one or more of the following:

* Style the appearance using css

* Extend standard plugins

* Add custom plugins



How to add support for a new css framework
******************************************

