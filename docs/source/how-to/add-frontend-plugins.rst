.. _how-to-add-frontend-plugins:

How to add your own frontend plugin
===================================

Creating the plugin
-------------------

In order to integrate your custom plugins with Django CMS Frontend within your Django app, you should follow these steps.

1. **Define a Plugin Model**:As the first step, you need to define a model for your plugin. This is done in the `models.py` of your Django app. The Plugin model needs to be a **proxy model** of the Django CMS Frontend's `FrontendUIItem` class.

The plugin model defines what kind information will be associated with instances of your plugin.

   Here is an example of a hypothetical plugin model:

   .. code-block:: python

       # models.py
       from djangocms_frontend.models import FrontendUIItem


       class YourPluginModel(FrontendUIItem):
           class Meta:
               proxy = True  # MUST be a proxy model
               verbose_name = _("Your Plugin")

           def short_description(self):
               return f"'{self.field_name}'"

   In this example, the `YourPluginModel` is a proxy of the `FrontendUIItem`, which is the base class for all Django CMS Frontend plugins. It includes a short description method that provides a description for each instance of the plugin.

   .. note::

      Keep in mind proxy models don't allow adding fields to the model. If your plugin needs to include additional fields, consider using  ``AbstractFrontendUIItem`` as the base class and remove ``proxy = True`` from the Meta class.

2. **Define a Plugin Form**: This form will declare which data to store in the
   ``FrontendUIItem``'s JSON field. The ``EntangledModelForm`` will automatically
   store the data in the JSON field. The ``untangled_fields`` attribute can be used
   to define fields that should be stored as regular model fields. This is useful
   for fields that are used in the frontend, but not in the backend. The
   ``untangled_fields`` attribute is optional.

   It will be used in the frontend to create and edit plugin instances.

2. **Define a Plugin Form**: You should also define a form that will instruct Django on how to handle the input for creating and editing instances of your plugin. The form should specify which data will be stored in the `FrontendUIItem`'s JSON field.

   Here is an example of a form for the `YourPluginModel`:

   .. code-block:: python

        # forms.py
        from django import forms
        from djangocms_frontend.models import FrontendUIItem
        from entangled.forms import EntangledModelForm

        class YourPluginForm(EntangledModelForm):
            class Meta:
                model = FrontendUIItem
                entangled_fields = {
                    "config": [
                        "field_name",  # This field will be stored in the config JSON
                     ]
                }
                # untangled_fields = ("tag_type",)  # Only if you use the tag_type field
            field_name = forms.CharField(max_length=50)

3. **Create a Plugin Class**: In the same app, create a file named ``cms_plugins.py``.
   Inside this file, define a class for your plugin by extending ``CMSPluginBase``.

   .. code-block:: python

       # cms_plugins.py
       from djangocms_frontend.cms_plugins import CMSUIPlugin
       from cms.plugin_pool import plugin_pool
       from . import models, forms


       @plugin_pool.register_plugin
       class YourPlugin(CMSUIPlugin):
           model = models.YourPluginModel
           form = forms.YourPluginForm
           name = "Your Plugin Name"
           render_template = "your_plugin_template.html"

           fieldsets = [
               # All fields must be listed in the form, either as entangled or untangled
               # fields.
               (None, {
                   "fields": [
                       "field_name",
                   ]
               }),
           ]

           def render(self, context, instance, placeholder):
               context.update({"instance": instance})
               return context

4. **Create a Plugin Template**: Create an HTML template for your plugin in your app's
   ``templates`` directory. This template will define how your plugin is rendered on the
   page.

   .. code-block:: html

       <!-- your_plugin_template.html -->
       <div class="your-plugin-class">
           {{ instance.field_name }} or {{ instance.config.field_name }}
       </div>

   The "entangled" fields in the JSON config can either be accessed  using
   ``instance.config.field_name`` or by using the ``instance.field_name`` syntax. The
    latter is only possible if the field model does not have a property with the same
    name.

Remember, developing custom plugins requires a good understanding of Django's and Django
CMS's architecture. Additionally, consider the security implications of your plugin,
especially if it handles user input.



Extending the plugin
--------------------

django CMS Frontend comes with a set of mixins that can be used to extend the
functionality of your plugin. These mixins are:

* **Attributes**: Adds a set of attributes to the plugin. Attributes are key-value
  pairs that can be used to store additional data in the plugin. Attributes are
  stored in the ``attributes`` JSON field of the ``FrontendUIItem`` model.
* **Background**: Adds background formatting to the plugin.
* **Responsive**: Adds responsive formatting to the plugin.
* **Spacing**: Adds spacing formatting to the plugin.
* **Sizing**: Adds sizing formatting to the plugin.
* **Title**: Adds an optional title to the plugin which can be used to display
  a title above the plugin or just to simplify the navigation of the plugin tree.

Each mixin comes in two flavours, one for the plugin and one for the plugin form.
The plugin mixin is used to add the functionality to the plugin, while the form
mixin is used to add their fields to the plugin form. The mixins are
designed to be used together.

For example, if you want to use the attributes mixin, you need to add the
``AttributesMixin`` to your plugin and the ``AttributesMixinForm`` to your
plugin form::

    from djangocms_frontend.cms_plugins import AttributesMixin, AttributesMixinForm

    class YourPlugin(AttributesMixin, CMSUIPlugin):
        ...

    class YourPluginForm(AttributesMixinForm, EntangledModelForm):
        ...

Re-using links and images
-------------------------

django CMS Frontend comes with a set of classes that can be used to re-use links
and images in your plugin. These mixins are:

* **LinkPluginMixin**: Adds a link to the plugin. The link can be used to link
  the plugin to a page, a file or an external URL. Include **GetLinkMixin** with
  your plugin model and base the admin form on **AbstractLinkForm** (can also
  be used as a mixin)::

        from djangocms_frontend.contrib.link.cms_plugins import LinkPluginMixin
        from djangocms_frontend.contrib.link.models import GetLinkMixin
        from djangocms_frontend.contrib.link.forms import AbstractLinkForm

        class YourPlugin(LinkPluginMixin, CMSUIPlugin):
            ...

        class YourPluginForm(AbstractLinkForm):
            link_is_optional = False  # True, if the link is optional
            ...

        class YourPluginModel(GetLinkMixin, FrontendUIItem):
            ...

  The resolved link (final URL) will be passed as ``mixin_link`` to the plugin context.


* **ImageMixin**: Adds an image to the plugin *model*. Base your plugin form on
  **ImageForm** (can also be used as a mixin)::

        from djangocms_frontend.contrib.image.models import ImageMixin
        from djangocms_frontend.contrib.image.forms import ImageForm

        class YourPluginForm(ImageForm):
            ...

        class YourPluginModel(ImageMixin, FrontendUIItem):
            image_field = "image"  # The name of the image field in the config JSON
            ...

