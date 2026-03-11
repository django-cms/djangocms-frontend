******
Models
******

``djangocms-frontend`` subclasses the ``CMSPlugin`` model.

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
    field (stored in ``.config``). The ``class`` attribute reflects all
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
