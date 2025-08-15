.. _inline_editing_custom_components:

#########################################################
How to Use Inline Editing with Custom Frontend Components
#########################################################

.. versionadded:: 2.0

``djangocms-frontend`` introduces simplified support for **inline editing** in custom
components, making it easier to edit content directly on the page without opening the
plugin'S change form. This guide will walk you through using the ``inline_field``
template tag to enable inline editing for your custom frontend components.

.. note::

    Inline editing requires djangocms-text to be installed and configured in your project.


Understanding the ``inline_field`` Template Tag
===============================================

The ``inline_field`` template tag allows you to make specific fields editable directly from
the page. It works by wrapping a field in an inline editing context, which is recognized by
django CMS's edit mode.

Syntax:

.. code-block:: django

    {% load frontend %}
    {% inline_field instance "field_name" %}

- ``instance`` - The plugin or model instance.
- ``"field_name"`` - The name of the field you want to make editable inline.

If the instance is called ``"instance"`` in the context, the tag can be abbreviated by
``{% inline_field "field_name" %}``.

When the page is in edit mode, the template tag will render the field as an editable text
input. If not in edit mode the template tag will render the field as plain text.

.. note::

    The ``inline_field`` tag is only available for fields that are explicitly listed in
    the ``frontend_editable_fields`` property of the plugin. When run in a template component,
    the tag will automatically register the field with the list of editable fields.

    The tag itself is a shortcut for django CMS's ``render_model`` tag. Since django CMS 5, this
    tags works for all CMS plugins (and not only for third-party models). For earlier versions
    of django CMS ``djangocms-frontend`` includes a custom extension for frontend plugins to
    support inline editing.


Step-by-Step: Adding Inline Editing to a custom frontend component
==================================================================

1. **Define Your Custom Component Plugin**

   First, create a djangoCMS plugin for your custom frontend component. Example:

   .. code-block:: python

       from cms.plugin_base import CMSPluginBase
       from cms.plugin_pool import plugin_pool
       from django.utils.translation import gettext_lazy as _
       from djangocms_frontend.models import FrontendUIItem

       class CustomComponentPlugin(CMSPluginBase):
           model = FrontendUIItem  # Base model
           name = _("Custom Component")
           module = _("Frontend")
           render_template = "frontend/custom_component.html"

       plugin_pool.register_plugin(CustomComponentPlugin)

2. **Modify the Component Template to Support Inline Editing**

   Open the template file (``frontend/custom_component.html``) and update it using the
   ``inline_field`` tag:

   .. code-block:: django

       {% load frontend %}

       <div class="custom-component">
           <h2>{% inline_field instance "title" %}</h2>
           <p>{% inline_field instance "description" %}</p>
       </div>

3. **Explicitly allow the field for inline editing**

   In the plugin definition, add the field to the ``frontend_editable_fields`` list:

   .. code-block:: python

        class CustomComponentPlugin(CMSPluginBase):
           model = FrontendUIItem  # Base model
           name = _("Custom Component")
           module = _("Frontend")
           render_template = "frontend/custom_component.html"
           frontend_editable_fields = ["title", "description"]

4. **Test Inline Editing**

   - Run the Django server:

     .. code-block:: bash

        python manage.py runserver

   - Log in as an admin user and enter **Edit Mode**.
   - Add your custom frontend component to a page.
   - Click on the text fields to edit them inline.
   - Leave the field, and changes will be stored automatically in the database.


Additional Considerations
=========================

- **Rich Text Editing:** If the field is a ``HTMLField``, django CMS text will automatically use
  a rich text editor for inline editing.
- **CSS & JavaScript Adjustments:** In rare cases custom frontend component's styles can interfere
  with django CMS text's inline editing interface. More specific rules typically solve the issue.
