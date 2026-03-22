*************
Template tags
*************

``djangocms-frontend`` provides template tags for rendering components and slots.
Load them with ``{% load frontend %}``.

.. py:function:: childplugins

    Template tag for rendering child plugins of a component instance. This is the primary
    way to render slot content in component templates.

    **Basic usage:**

    .. code-block:: django

        {% load frontend %}
        
        {# Render all child plugins #}
        {% childplugins instance %}
        
        {# Render plugins in a specific slot #}
        {% childplugins instance "buttons" %}

    **With fallback content:**

    You can provide fallback content that displays when the slot is empty:

    .. code-block:: django

        {% childplugins instance "buttons" or %}
            <button>Default Button</button>
        {% endchildplugins %}

    **Declaring slots in component definitions:**

    When used with both slot name and verbose name in a component template during
    registration, it declares a new slot:

    .. code-block:: django

        {% childplugins instance "buttons" "Action Buttons" %}
            <!-- Fallback content -->
        {% endchildplugins %}

    **Parameters:**

    :param instance: The component plugin instance (optional, defaults to ``instance`` from context)
    :param plugin_type: Slot name or plugin type to filter (optional)
    :param verbose_name: Verbose name for slot declaration (optional, used during component registration)

    **Behavior:**

    - If ``plugin_type`` is provided without "Plugin" suffix, it treats it as a slot name and
      automatically constructs the full plugin type name
    - Renders all matching child plugins using their respective templates
    - If a block with fallback content is provided (using ``or``), it displays when no plugins match
    - During component registration, declaring slots with verbose names automatically adds them
      to the component's slot configuration

    See also :ref:`components-with-slots` for detailed slot usage examples.

.. py:function:: plugin

    Template tag for rendering a plugin instance without saving it to the database. This is
    useful for creating demo content, prototyping, or rendering plugins programmatically.

    **Basic usage:**

    .. code-block:: django

        {% load frontend %}
        
        {# Render a plugin with default settings #}
        {% plugin "GridContainer" %}
        
        {# Render with custom parameters #}
        {% plugin "GridRow" container_fluid=True %}
        
        {# Store rendered output in a variable #}
        {% plugin "Alert" alert_context="info" alert_dismissable=True as my_alert %}
        {{ my_alert }}

    **With child content:**

    .. code-block:: django

        {% plugin "Card" card_alignment="left" %}
            <h3>Card Title</h3>
            <p>Card content goes here</p>
        {% endplugin %}

    **Parameters:**

    :param name: The plugin name (must be registered in ``CMS_COMPONENT_PLUGINS`` setting)
    :param kwargs: Keyword arguments matching the plugin's form fields
    :param as varname: Optional variable name to store the rendered output

    **Requirements:**

    - The plugin must be listed in the ``CMS_COMPONENT_PLUGINS`` setting
    - Plugin templates are compiled at startup for performance
    - Child content can be provided between ``{% plugin %}...{% endplugin %}`` tags

    .. note::
       The ``{% plugin %}`` tag creates a temporary instance that is never saved to the
       database. This makes it ideal for testing and prototyping but should not be used
       for production content that needs to be editable by content editors.

.. py:function:: slot

    Template tag used within ``{% plugin %}...{% endplugin %}`` blocks to define boundaries
    for different slots when testing multi-slot components.

    **Usage:**

    .. code-block:: django

        {% load frontend %}
        
        {% plugin "Card" %}
            {% slot "header" %}
                <h3>Card Header</h3>
            {% endslot %}
            
            {% slot "body" %}
                <p>Card body content</p>
            {% endslot %}
            
            {% slot "footer" %}
                <small>Card footer</small>
            {% endslot %}
        {% endplugin %}

    **Parameters:**

    :param slot_name: The name of the slot (must match a slot defined in the component)

    **Behavior:**

    - Creates dummy plugin instances for each slot
    - Content between ``{% slot %}...{% endslot %}`` is assigned to that slot
    - Only works within ``{% plugin %}`` blocks
    - The slot tag itself doesn't render anything; child plugins are rendered by ``{% childplugins %}``

    This is primarily used for testing and demonstrating components with multiple slots.

.. py:function:: inline_field

    Template tag that enables inline editing of plugin fields in django CMS edit mode.
    This allows editors to edit field values directly in the frontend without opening
    the plugin edit dialog.

    **Basic usage:**

    .. code-block:: django

        {% load frontend %}
        
        {# Edit a specific field of the current instance #}
        {% inline_field instance "title" %}
        
        {# Shortcut: instance from context #}
        {% inline_field "title" %}
        
        {# With custom filters #}
        {% inline_field instance "content" filters="safe|linebreaks" %}

    **Parameters:**

    :param instance: The plugin instance to edit (optional if ``instance`` is in context)
    :param attribute: The field name to make editable
    :param language: Language code for multilingual fields (optional)
    :param filters: Template filters to apply to the field value (optional)
    :param view_url: Custom URL for the edit view (optional)
    :param view_method: Custom view method (optional)

    **Behavior:**

    - In edit mode: Wraps the field in an editable interface with save/cancel buttons
    - In live mode: Simply displays the field value
    - During component registration: Automatically registers the field as editable
    - Only works with saved plugin instances (requires a primary key)

    **Example in a component template:**

    .. code-block:: django

        <div class="card">
            <h3>{% inline_field "title" %}</h3>
            <div>{% inline_field "content" filters="safe" %}</div>
        </div>

    .. note::
       Inline editing only activates when the django CMS toolbar is in edit mode
       and the plugin has been saved to the database. It will not work with
       dummy plugins created via the ``{% plugin %}`` tag.
