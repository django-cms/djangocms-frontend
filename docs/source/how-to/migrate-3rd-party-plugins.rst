How to migrate other plugin packages
====================================

The management command ``migrate`` converts any plugin from **djangocms_bootstrap4** and
**djangocms_styled_link** to ``djangocms-frontend``. This behaviour can be extended
adding custom migratation modules to the ``DJANGOCMS_FRONTEND_ADDITIONAL_MIGRATIONS``
setting.

A migration module must contain this three objects:

plugin_migrations
    Dictionary with the configuration of migration process for each plugin class.

data_migration
    Dictionary with methods to transform attributes of the plugins.

plugin_prefix
    String with the prefix of the plugin_types that are being migrated. The migration
    process alerts if there are remaining plugins with this prefix.

Check the source code of ``management/bootstrap4_migration.py`` to get more details
about this three objects.
