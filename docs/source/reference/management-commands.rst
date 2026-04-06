*******************
Management commands
*******************

Management commands are run by typing ``python -m manage frontend command`` in the
project directory. ``command`` can be one of the following:

``migrate``
    Migrates plugins from other frontend packages to ``djangocms-frontend``.
    Currently supports **djangocms_bootstrap4** and **djangocms_styled_link**.
    Other packages can be migrated adding custom migration modules to
    the ``DJANGOCMS_FRONTEND_ADDITIONAL_MIGRATIONS`` setting.

``stale_references``
    If references in a UI item are moved or removed the UI items are designed to
    fall back gracefully and both not throw errors or be deleted themselves
    (by a db cascade).

    The drawback is, that references might become stale. This command prints all
    stale references, their plugins and pages/placeholder they belong to.

.. _sync_permissions:

``sync_permissions``
    This command syncs permissions for users or groups. It is run with one of
    the following arguments:

    - ``users``: Syncs permissions for all users.
    - ``groups``: Syncs permissions for all groups.

    Permissions are copied from the ``FrontendUIItem`` model to all installed
    plugins. This way you can set permissions for all plugins by setting them
    for ``FrontendUIItem`` and then syncing them.

.. _clear_advanced_settings:

``clear_advanced_settings``
    Removes all advanced settings from every djangocms-frontend plugin instance
    in the database. Specifically it:

    - Clears the ``attributes`` config (custom HTML attributes and classes) on
      each plugin.
    - Resets ``tag_type`` to the default value (``div``) for every plugin whose
      tag type was changed.

    This is useful after setting
    :py:attr:`~settings.DJANGOCMS_FRONTEND_SHOW_ADVANCED_SETTINGS` to
    ``False`` to ensure no orphaned advanced settings remain in the database.

    Run with ``--noinput`` to skip the confirmation prompt::

        python -m manage frontend clear_advanced_settings --noinput

``rename``
    Renames a plugin type in the database. This is useful when a plugin has been
    replaced by a new one and existing instances need to be reassigned. This comand
    is intended for djangocms-frontend plugins which share the same plugin model
    (:class:`AbstractFrontendUIItem`). Hence, model instances are not created, so only
    apply this command to non-frontend plugins if you know what you're doing.

    It takes two positional arguments:

    - ``old_plugin``: The plugin type to rename. Must **not** be installed but
      must still be present in the database.
    - ``new_plugin``: The plugin type to rename to. Must be installed.

    The command updates the ``plugin_type`` field on all matching ``CMSPlugin``
    rows. If the new plugin's model is a subclass of ``AbstractFrontendUIItem``,
    the ``ui_item`` field is updated as well.

    Example::

        python -m manage frontend rename OldCardPlugin CardPlugin
