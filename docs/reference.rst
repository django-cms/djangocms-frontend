###########
 Reference
###########

**********
 Settings
**********

Available settings will be revised. For now only the following can be
changed:

.. py:attribute:: settings.DJANGOCMS_FRONTEND_TAG_CHOICES

    Defaults to ``['div', 'section', 'article', 'header', 'footer', 'aside']``.

    Lists the choices for the tag field of all djangocms-frontend plugins.
    ``div`` is the default tag.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_GRID_SIZE

    Defaults to ``12``.


.. py:attribute:: settings.DJANGOCMS_FRONTEND_GRID_CONTAINERS

    Default:

    .. code::

        (
           ('container', _('Container')),
           ('container-fluid', _('Fluid container')),
           ("container-sm", _("sx container")),
           ("container-md", _("md container")),
           ("container-lg", _("lg container")),
           ("container-xl", _("xl container")),
       )

.. py:attribute:: settings.DJANGOCMS_FRONTEND_USE_ICONS

    Defaults to ``True``.

    Decides if icons should be offered, e.g. in links.

.. py:attribute:: settings.DJANGOCMS_FRONTEND_CAROUSEL_TEMPLATES

   Defaults to ``(('default', _('Default')),)``

.. py:attribute:: settings.DJANGOCMS_FRONTEND_TAB_TEMPLATES

   Defaults to ``(('default', _('Default')),)``



.. py:attribute:: settings.DJANGOCMS_FRONTEND_SPACER_SIZES

    Default:

    .. code::

        (
           ('0', '* 0'),
           ('1', '* .25'),
           ('2', '* .5'),
           ('3', '* 1'),
           ('4', '* 1.5'),
           ('5', '* 3'),
       )

.. py:attribute:: settings.DJANGOCMS_FRONTEND_CAROUSEL_ASPECT_RATIOS

    Default: ``((16, 9),)``

    Additional aspect ratios offered in the carousel component

.. py:attribute:: settings.DJANGOCMS_FRONTEND_COLOR_STYLE_CHOICES

    Default:

    .. code::

        (
           ('primary', _('Primary')),
           ('secondary', _('Secondary')),
           ('success', _('Success')),
           ('danger', _('Danger')),
           ('warning', _('Warning')),
           ('info', _('Info')),
           ('light', _('Light')),
           ('dark', _('Dark')),
           ('custom', _('Custom')),
       )

.. py:attribute:: TEXT_SAVE_IMAGE_FUNCTION

    Requirement: ``TEXT_SAVE_IMAGE_FUNCTION = None``

    .. warning::

        Please be aware that this package does not support
        djangocms-text-ckeditor's `Drag & Drop Images
        <https://github.com/divio/djangocms-text-ckeditor/#drag--drop-images>`_
        so be sure to set ``TEXT_SAVE_IMAGE_FUNCTION = None``.


******
Models
******

**djangocms-frontend** subclasses the ``CMSPlugin`` model.

.. py:class:: FrontendUIItem(CMSPlugin)

    Import from ``djangocms_frontend.models``.

    All concrete models for UI items are proxy models of this class.
    This implies you can create, delete and update instances of the proxy models
    and all the data will be saved as if you were using this original
    (non-proxied) model.

    This way all proxies can have different python methods as needed while still
    all using the single database table of ``FrontendUIItem``.

.. py:attribute:: FrontendUIItem.ui_item

    This CharField contains the UI item's type without the suffix "Plugin",
    e.g. "Link" and not "LinkPlugin". This is a convenience field. The plugin
    type is determined by ``CMSPlugin.plugin_type``.

.. py:attribute:: FrontendUIItem.tag_type

    This is the tag type field determining what tag type the UI item should have.
    Tag types default to ``<div>``.

.. py:attribute:: FrontendUIItem.config

    The field ``config`` is the JSON field that contains a dictionary with all specific
    information needed for the UI item. The entries of the dictionary can be
    directly **read** as attributes of the ``FrontendUIItem`` instance. For
    example, ``ui_item.context`` will give ``ui_item.config["context"]``.

    .. warning::

        Note that changes to the ``config`` must be written directly to the
        dictionary:  ``ui_item.config["context"] = None``.


.. py:method:: FrontendUIItem.add_classes(self, *args)

    This helper method allows a Plugin's render method to add framework-specific
    html classes to be added when a model is rendered. Each positional argument
    can be a string for a class name or a list of strings to be added to the list
    of html classes.

    These classes are **not** saved to the database. They merely a are stored
    to simplify the rendering process and are lost once a UI item has been
    rendered.

.. py:method:: FrontendUIItem.get_attributes(self)

    This method renders all attributes given in the optional ``attributes``
    field (stored in ``.config``). The ``class`` attriubte reflects all
    additional classes that have been passed to the model instance by means
    of the ``.add_classes`` method.

.. py:method:: FrontendUIItem.initialize_from_form(self, form)

    Since the UIItem models do not have default values for the contents of
    their ``.config`` dictionary, a newly created instance of an UI item
    will not have config data set, not even required data.

    This method initializes all fields in ``.config`` by setting the value to
    the respective ``initial`` property of the UI items admin form.

.. py:method:: FrontendUIItem.get_short_description(self)

    returns a plugin-specific short description shown in the structure mode
    of django CMS.

*********************
 Management commands
*********************

Management commands are run by typing ``./manage.py command`` in the project
directory.

``migrate_frontend``
    Migrates plugins from other frontend packages to **djangocms-frontend**.
    Currently supports **djangocms-bootstrap4** and **djangocms_styled_link**.

``stale_frontend_references``
    If references in a UI item are moved or removed, the UI items are designed to
    fall back gracefully and both not throw errors or be deleted themselves
    (by a db cascade).

    The drawback is, that references might become stale. This command prints all
    stale references, their plugins and pages/placeholder they belong to.


***************
 Running Tests
***************

You can run tests by executing:

.. code::

   virtualenv env
   source env/bin/activate
   pip install -r tests/requirements.txt
   python ./run_tests.py

