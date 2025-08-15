
.. _components:

How to use frontend plugins as components in templates
======================================================

.. versionadded:: 2.0

The plugins of ``djangocms-frontend`` can be used as components in your
templates - even in apps that do not use or integrate with django CMS
otherwise. This is useful if you want use exactly the same markup for, say,
buttons, links, the grid both in pages managed with django CMS and in
other parts of your project without duplicating HTML code.

This feature introduces a simple and flexible way to reuse django CMS
plugins directly in templates without needing to create database entries for
them. This allows developers to maintain clean, reusable, and dynamic
components, such as buttons, cards, links, and more, while minimizing code
repetition.

.. note::

    To make plugins available as components, ensure that the
    ``CMS_COMPONENT_PLUGINS`` setting in your project's ``settings.py``
    is a list that includes the necessary plugin names or dotted path to
    a plugin parent class. Only plugins named in the listing or their
    child classes can be used directly in templates
    without creating database entries.

    * To include all ``djangocms-frontend`` plugins, use
      ``djangocms_frontend.cms_plugins.CMSUIPlugin`` in the setting.

    * To include all :ref:`custom components <custom_components>`, use
      ``djangocms_frontend.ui_plugin_base.CMSUIComponent`` in the setting.

To use a frontend plugin in a template you need to load the ``frontend`` tags
and then use the ``plugin`` template tag to render a frontend plugin.

.. code::

    {% load frontend %}
    {% plugin "alert" alert_context="secondary" alert_dismissable=True %}
        Here goes the content of the alert.
    {% endplugin %}

The plugins will be rendered based on their standard attribute settings.
You can override these settings by passing them as keyword arguments to the
``plugin`` template tag.

You can also create more complex reusable components, like a card with inner
elements such as headers, bodies, and lists, by nesting plugins. Here’s an
example of a card component::

    {% load frontend %}
    {% plugin "card" card_alignment="center" card_outline="info" card_text_color="primary" card_full_height=True %}
        {% plugin "cardinner" inner_type="card-header" text_alignment="start" %}
            <h4>Card title</h4>
        {% endplugin %}
        {% plugin "cardinner" inner_type="card-body" text_alignment="center" %}
            Some quick example text to build on the card title and make up the bulk of the card's content.
        {% endplugin %}
        {% plugin "listgroupitem" %}An item{% endplugin %}
        {% plugin "listgroupitem" %}A second item{% endplugin %}
        {% plugin "listgroupitem" %}A third item{% endplugin %}
    {% endplugin %}

Breakdown of the Code:

* ``plugin "card"``: Creates the outer card component.
    * ``card_alignment="center"``: Aligns the card content to the center.
    * ``card_outline="info"``: Gives the card an "info" outline style.
    * ``card_text_color="primary"``: Changes the text color to "primary."
    * ``card_full_height=True``: Ensures the card takes up the full height of its container.
* Nested ``plugin "cardinner"``: Creates inner components within the card.
    * ``inner_type="card-header"``: Specifies a header section for the card.
    * ``text_alignment="start"``: Aligns the header text to the start (left).
* Additional nested ``plugin "cardinner"`` and ``listgroupitem``:
* These create the body of the card and a list group inside the card.

The above template generates a dynamic card component with a header, a body,
and a list group that can be reused across multiple pages without requiring
database entries.

For more examples, see the documentation of the djanog CMS plugins on of how to
use the ``{% plugin %}`` template tag with each plugin.


.. note::

    While this is designed for ``djangocms-frontend`` plugins primarily, it
    will work with many other django CMS plugins.

    Since no plugins are created in the database, plugins relying on their
    instances being available in the database will potentially not work.


.. warning::

    Currently, ``{% placeholder %}`` template tags are not supported inside
    a ``{% plugin %}`` tag. This is because the ``{% plugin %}`` tag does
    preprocess the content and placeholders are not recognized by django CMS.


Multi-line tags
---------------

Multi-line tags are not supported in Django templates. For components with many
parameters this can lead to long lines of code. To make the code more readable
you can use the following patch (to be executed, for example during your project's
``AppConfig.ready()`` method):

.. code-block:: python

    import re
    from django.template import base

    base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)

This will patch the Django template engine **for all templates rendered by it
within your project.** It will however allow templates like this:

.. code-block:: django

    {% plugin "card"
        card_alignment="center"
        card_outline="info"
        card_text_color="primary"
        card_full_height=True %}
        ...
    {% endplugin %}

