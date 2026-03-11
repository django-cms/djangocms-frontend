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
