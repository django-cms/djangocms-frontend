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
