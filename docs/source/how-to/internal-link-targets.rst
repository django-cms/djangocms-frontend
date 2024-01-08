.. _how to add internal link targets outside of the cms:

**************************************************
 How to add internal link targets outside the CMS
**************************************************

By default the link/button component offers available CMS pages of the
selected language as internal links.

The developer may extend this setting to include other page-generating
Django models as well by adding the ``DJANGOCMS_FRONTEND_LINK_MODELS``
setting to the project's ``settings.py`` file.

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

.. code:: python

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

.. code:: python

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

.. index::
    single: Extend plugins
