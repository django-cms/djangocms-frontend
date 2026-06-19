*****************
Template filters
*****************

``djangocms-frontend`` provides template filters that can be used in component templates.
Load them with ``{% load frontend %}``.

.. py:function:: get_slot(instance, slot_name)

    Import from ``djangocms_frontend.templatetags.frontend``.

    Get plugins for a specific slot directly from a component instance. This is useful 
    for manually iterating over slot plugins in a component's template instead of using 
    the ``{% childplugins %}`` template tag.

    :param instance: The component plugin instance
    :param slot_name: The name of the slot to retrieve plugins from
    :return: Generator yielding child plugin instances in the specified slot

    **Usage in templates:**

    .. code-block:: django

        {% load frontend %}
        
        {% for plugin in instance|get_slot:"buttons" %}
            {# Manually render each plugin in the slot #}
            <div class="button-wrapper">
                {% render_plugin plugin %}
            </div>
        {% endfor %}

    This is useful when you need more control over how slot content is rendered,
    compared to the ``{% childplugins %}`` tag which handles rendering automatically.

.. py:function:: children(instance, plugin_type=None)

    .. versionadded:: 2.5

    Import from ``djangocms_frontend.templatetags.frontend``.

    Get the direct child plugin **instances** of a component, optionally filtered
    by component (plugin) type. Unlike :func:`get_slot`, which digs into a named
    slot, ``children`` returns the component's own children; unlike
    ``{% childplugins %}``, which returns rendered HTML, it returns the instances
    themselves. That lets a template iterate the same children more than once — a
    tab nav and the tab panes, say — and render their fields and bodies themselves.

    The ``plugin_type`` may be given with or without the ``Plugin`` suffix, so
    both ``"TabItem"`` and ``"TabItemPlugin"`` resolve to the same type. Omitting
    it returns every child. The return value is a re-iterable tuple, and it is
    safe to use while a component template is being scanned for declaration (an
    instance without children simply yields nothing).

    :param instance: The component plugin instance
    :param plugin_type: Optional component/plugin name to filter by
    :return: Tuple of matching child plugin instances, in order

    **Usage in templates:**

    .. code-block:: django

        {% load frontend cms_tags %}

        <ul class="nav" role="tablist">
            {% for item in instance|children:"TabItem" %}
                <li>{{ item.tab_title }}</li>
            {% endfor %}
        </ul>
        <div class="tab-content">
            {% for item in instance|children:"TabItem" %}
                {% render_plugin item %}
            {% endfor %}
        </div>

    This is the natural companion to :ref:`nested components <nested_components>`,
    where a parent component renders its repeating, typed children.

.. py:function:: get_attributes(attribute_field, *add_classes)

    Simple tag that joins classes with an attributes field and returns all HTML attributes
    formatted for use in templates.

    :param attribute_field: Dictionary of HTML attributes (e.g., ``{"class": "btn", "id": "my-id"}``)
    :param add_classes: Additional CSS classes to merge with existing ones
    :return: Safe HTML string of formatted attributes

    **Usage in templates:**

    .. code-block:: django

        {% load frontend %}
        
        {# Basic usage with attributes field #}
        <div {% get_attributes instance.attributes %}>
        
        {# Add additional classes #}
        <div {% get_attributes instance.attributes "extra-class" "another-class" %}>
        
        {# Combine multiple class sources #}
        <button {% get_attributes instance.attributes some_variable "static-class" %}>

    **Behavior:**

    - Merges all provided classes into a single ``class`` attribute
    - Properly escapes attribute values for safety
    - Handles boolean attributes (renders just the attribute name if value is empty)
    - Returns a safe HTML string that can be used directly in templates
