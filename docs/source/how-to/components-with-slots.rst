.. _components-with-slots:

####################################
Creating Components with Slots
####################################

.. index::
    single: Components with slots
    single: Slots

.. versionadded:: 2.0

Slots allow you to define specific regions within a component where content editors can add child plugins. This is useful when you want to control the structure of a component while allowing flexibility in certain areas.


What are slots?
===============

Slots are predefined placeholders in a component that:

- Automatically create child plugin types for each slot
- Restrict where child plugins can be added
- Provide fallback content when a slot is empty
- Are automatically created when a component instance is saved


Defining slots
==============

To define slots in your component, add a ``slots`` attribute to the component's ``Meta`` class:

.. code-block:: python

    from django import forms
    from djangocms_frontend.component_base import CMSFrontendComponent, Slot
    from djangocms_frontend.component_pool import components
    from djangocms_frontend.contrib.image.fields import ImageFormField

    @components.register
    class MyHero(CMSFrontendComponent):
        class Meta:
            name = "My Hero Component"
            render_template = "hero.html"
            slots = (
                ("title", "Title"),      # (slot_name, verbose_name)
                ("slot", "Slot"),
            )
        
        title = forms.CharField(required=True, initial="my title")
        slogan = forms.CharField(
            required=True, 
            initial="django CMS' plugins are great components", 
            widget=forms.Textarea
        )
        image = ImageFormField(required=True)
        
        def get_short_description(self):
            return self.title

**Slot definition formats:**

Simple tuple format::

    slots = (
        ("slot_name", "Verbose Name"),
        ("buttons", "Buttons"),
    )

Using the Slot class for advanced options::

    from djangocms_frontend.component_base import Slot
    
    slots = (
        Slot("slot_name", "Verbose Name", allow_children=False),
        Slot("buttons", "Buttons", **additional_plugin_kwargs),
    )


Using slots in templates
=========================

In your render template, use the ``{% childplugins %}`` template tag to render slot content:

.. code-block:: django

    {% load cms_tags frontend sekizai_tags %}
    
    <section class="bg-white dark:bg-gray-900">
        <div class="grid max-w-screen-xl px-4 py-8 mx-auto">
            <div class="mr-auto place-self-center">
                <h1>
                    {% childplugins instance "title" %}
                        <!-- Fallback content if slot is empty -->
                        {{ instance.title }}
                    {% endchildplugins %}
                </h1>
                <p>
                    {% childplugins instance "slogan" %}
                        {{ instance.slogan }}
                    {% endchildplugins %}
                </p>
                
                {% childplugins instance "slot" %}
                    <!-- Default content for empty slots -->
                    <a href="#" class="btn btn-primary">
                        Get started
                    </a>
                {% endchildplugins %}
            </div>
        </div>
    </section>

The content between ``{% childplugins %}`` and ``{% endchildplugins %}`` serves as fallback content that will be displayed when the slot has no child plugins.

For complete ``{% childplugins %}`` tag documentation, see the :ref:`reference documentation <Template tags>`.


How slots work
==============

When you define slots in a component:

1. **Child plugin classes are created automatically**: For a component named ``MyHero`` with a slot named ``title``, a plugin class ``MyHeroTitlePlugin`` is automatically generated.

2. **Parent-child relationships are enforced**: Slot plugins can only be added as children of their parent component.

3. **Auto-creation on save**: When a new component instance is created, all slot plugins are automatically added to it (see ``save_model`` in :class:`~djangocms_frontend.component_base.CMSFrontendComponent`).

4. **allow_children is set automatically**: When slots are defined, ``allow_children`` is automatically set to ``True`` on the component plugin.


Example with multiple slots
============================

Here's a more complex example with multiple slots:

.. code-block:: python

    @components.register
    class HeroWithSlots(CMSFrontendComponent):
        class Meta:
            name = "Hero with Slots"
            render_template = "hero_slots.html"
            slots = (
                ("title", "Title Slot"),
                ("subtitle", "Subtitle Slot"),
                ("buttons", "Button Area"),
                ("footer", "Footer Content"),
            )
        
        background_color = forms.CharField(required=False)
        hero_image = ImageFormField(required=True)

Template:

.. code-block:: django

    {% load cms_tags %}
    
    <section style="background-color: {{ instance.background_color }}">
        <div class="hero-content">
            <div class="hero-text">
                {% childplugins instance "title" %}
                    <h1>Default Title</h1>
                {% endchildplugins %}
                
                {% childplugins instance "subtitle" %}
                    <p>Default subtitle text</p>
                {% endchildplugins %}
                
                {% childplugins instance "buttons" %}
                    <button>Click Me</button>
                {% endchildplugins %}
            </div>
            
            <div class="hero-image">
                <img src="{{ instance.hero_image.url }}" alt="">
            </div>
        </div>
        
        <footer>
            {% childplugins instance "footer" %}
                <p>&copy; 2026 My Company</p>
            {% endchildplugins %}
        </footer>
    </section>


Advanced: Manual slot iteration with get_slot
==============================================

For more control over slot rendering, you can use the ``get_slot`` template filter to manually iterate over slot plugins:

.. code-block:: django

    {% load cms_tags frontend %}
    
    <section>
        <div class="buttons-container">
            {% for plugin in instance|get_slot:"buttons" %}
                <div class="button-wrapper">
                    {% render_plugin plugin %}
                </div>
            {% empty %}
                <p>No buttons added yet</p>
            {% endfor %}
        </div>
    </section>

The ``get_slot`` filter takes the slot name as an argument and returns a generator of child plugins in that slot. This is useful when you need to:

- Add custom wrapper HTML around each plugin in a slot
- Apply specific classes or attributes to individual slot items
- Implement complex layouts that require more control than ``{% childplugins %}`` provides
- Handle empty slots with custom logic using ``{% empty %}``

**Comparison:**

Using ``{% childplugins %}`` (automatic rendering with fallback):

.. code-block:: django

    {% childplugins instance "buttons" %}
        <button>Default Button</button>
    {% endchildplugins %}

Using ``get_slot`` filter (manual control):

.. code-block:: django

    {% for plugin in instance|get_slot:"buttons" %}
        <div class="custom-wrapper">
            {% render_plugin plugin %}
        </div>
    {% empty %}
        <button>Default Button</button>
    {% endfor %}

See also :py:func:`~djangocms_frontend.templatetags.frontend.get_slot` in the reference documentation.
