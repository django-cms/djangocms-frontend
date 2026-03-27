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
