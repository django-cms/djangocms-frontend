
.. index::
    single: Migration from Bootstrap 4
    single: migrate
    single: manage.py

.. _Migrating from djangocms-bootstrap4:

*************************************
 Migrating from djangocms-bootstrap4
*************************************

In the case you have a running django CMS project using
`djangocms-bootstrap4
<https://github.com/django-cms/djangocms-bootstrap4>`_ you can try to
run the automatic migration process. This process converts all plugin
instances of djangocms-bootstrap4 into corresponding djangocms-frontend
plugins.

.. note::

   Bootstrap 4 and Bootstrap 5 differ, hence even a  successful
   migration will require manual work to fix differences. The migration
   command is a support to reduce the amount of manual work. It will not
   do everything automatically!

   The more your existing installation uses the attributes field (found
   in "advanced settings") the more likely it is, that you will have to
   do some manual adjustment. While the migration command does adjust
   settings in the attributes field it cannot know the specifics of
   your project.

.. attention::

   Please do **back up** your database before you do run the management
   command!

For this to work, the both the ``djangocms-frontend`` **and** the
djangocms-bootstrap4 apps need to be included in ``INSTALLED_APPS``.

.. warning::

    The order of the apps in ``INSTALLED_APPS`` is **cruicial**.

    1. First is ``djangocms_link`` and ``djangocms_icon`` the first of which is needed by ``djangocms_bootstrap4``,
    2. then come all ``djangocms_bootstrap4`` plugins.
        ``djangocms_bootstrap4.contrib.bootstrap4_link`` uninstalls the Link
        plugin of ``djangocms_link``
    3. At last come all ``djangocms_frontend`` apps.

.. warning::

    The migration process does also migrate ``djangocms-icon`` instances to ``djangocms-frontend``. If you prefer to use ``djangocms-icon`` instead, remove ``"djangocms_frontend.contrib.icon"`` from installed apps.

.. code::

   ./manage.py cms delete-orphaned-plugins
   ./manage.py migrate
   ./manage.py frontend migrate

The migration process displays a counter indicating how many plugins were
converted (an integer like `2133` depending how many bootstrap4 plugins you have.):

        Migrating plugins
        =================
        Migrated 2133 plugins.
        Successfully migrated plugins.

        Checking installed apps for potential link destinations
        =======================================================
        No further link destinations found. Setup complete.

In the case that no plugins were migrated the output looks very similar but does
not contain the counter.

        Migrating plugins
        =================
        Nothing to migrate

        Checking installed apps for potential link destinations
        =======================================================
        No further link destinations found. Setup complete.

Only plugins managed by apps listed in ``INSTALLED_APPS`` will be migrated.

.. warning::

    Spin up your development server and test at this point if the migration
    has succeeded. Open a former djangocms-bootstrap4 plugin and check that
    it has the appearance of a dajngocms-frontend plugin.

Therefore only after you finish the migration you can remove all
djangocms-bootstrap4 apps **and** ``djangocms_link`` from ``INSTALLED_APPS``
and you may delete the now empty database tables of djangocms-bootstrap4.
You identify them by their name pattern:

.. code::

   bootstrap4_alerts_bootstrap4alerts
   bootstrap4_badge_bootstrap4badge
   ...
   bootstrap4_utilities_bootstrap4spacing
