.. _how-to-migrate-custom-plugins:

How to write migrations for custom plugins and components
=========================================================

When you rename, reorganize, or replace custom plugins and components, existing
plugin instances in the database still reference the old ``plugin_type``. A
Django data migration lets you update those references so that the CMS can find
the correct plugin class again.

This guide covers the two most common scenarios:

* Renaming a plugin (changing its class name or moving it to a different app).
* Replacing one plugin with another.

.. note::

   djangocms-frontend plugins share a single database table
   (``djangocms_frontend_frontenduiitem``) through proxy models.  This means
   renaming a plugin does **not** require any schema migration -- only the
   ``plugin_type`` (and optionally ``ui_item``) fields need to be updated.


Using the management command
----------------------------

For one-off renames that you run manually on each environment, the
``frontend rename`` management command is the quickest option::

    python -m manage frontend rename OldPlugin NewPlugin

See the :doc:`management commands reference <../reference/management-commands>`
for details and validation rules.


Writing a data migration
------------------------

If you want the rename to happen automatically when ``manage.py migrate`` is
run -- for example as part of a deployment pipeline -- wrap it in a Django data
migration.

Create an empty migration in your app::

    python -m manage makemigrations --empty yourapp -n rename_old_plugin

Then add the rename logic using ``RunPython``:

.. code-block:: python

    from django.db import migrations


    def rename_plugin(apps, schema_editor):
        CMSPlugin = apps.get_model("cms", "CMSPlugin")
        CMSPlugin.objects.filter(
            plugin_type="OldPlugin",
        ).update(plugin_type="NewPlugin")

        # Only needed if the plugin model is based on AbstractFrontendUIItem
        FrontendUIItem = apps.get_model("djangocms_frontend", "FrontendUIItem")
        FrontendUIItem.objects.filter(
            plugin_type="NewPlugin",
        ).exclude(
            ui_item="NewModel",
        ).update(ui_item="NewModel")


    def reverse_rename(apps, schema_editor):
        CMSPlugin = apps.get_model("cms", "CMSPlugin")
        CMSPlugin.objects.filter(
            plugin_type="NewPlugin",
        ).update(plugin_type="OldPlugin")

        FrontendUIItem = apps.get_model("djangocms_frontend", "FrontendUIItem")
        FrontendUIItem.objects.filter(
            plugin_type="OldPlugin",
        ).update(ui_item="OldModel")


    class Migration(migrations.Migration):
        dependencies = [
            ("yourapp", "0001_initial"),
            ("djangocms_frontend", "0001_initial"),
        ]

        operations = [
            migrations.RunPython(rename_plugin, reverse_rename),
        ]

Replace ``OldPlugin`` / ``NewPlugin`` with the actual ``plugin_type`` values
(typically the plugin class name, e.g. ``HeroPlugin``).  Replace ``OldModel`` /
``NewModel`` with the corresponding model class names (e.g. ``Hero``).

.. tip::

   Always provide a ``reverse_rename`` function so that the migration can be
   rolled back with ``manage.py migrate yourapp <previous_migration>``.


When to update ``ui_item``
--------------------------

The ``ui_item`` field only exists on models that inherit from
``AbstractFrontendUIItem`` (including ``FrontendUIItem`` proxy models and custom
components created with ``CMSFrontendComponent``).  If your plugin uses a
different model base -- or has no model at all -- skip the ``ui_item`` update.

+----------------------------------------------+----------------------------+
| Plugin base                                  | Update ``ui_item``?        |
+==============================================+============================+
| ``FrontendUIItem`` (proxy model)             | Yes                        |
+----------------------------------------------+----------------------------+
| ``AbstractFrontendUIItem`` (concrete model)  | Yes                        |
+----------------------------------------------+----------------------------+
| ``CMSFrontendComponent``                     | Yes                        |
+----------------------------------------------+----------------------------+
| ``CMSPluginBase`` with a custom model        | No                         |
+----------------------------------------------+----------------------------+
| Plugin with ``model = None``                 | No                         |
+----------------------------------------------+----------------------------+


Combining with schema migrations
---------------------------------

If your rename also involves schema changes (e.g. moving from a proxy model to
a concrete model with extra fields), put the data migration **between** the
schema migrations:

1. Schema migration that creates the new table or fields.
2. Data migration that copies/renames plugin instances.
3. Schema migration that removes the old table or fields (if any).

This ensures the data migration can read from the old structure and write to the
new one.
