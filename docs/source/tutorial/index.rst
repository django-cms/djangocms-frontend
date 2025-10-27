.. index::
    single: Tutorial

#################
 Getting Started
#################

When working with components in ``djangocms-frontend``, you can choose from different
approaches depending on your needs. These range from using built-in Bootstrap 5
components, over quick and simple methods to create your own custom frontend components to
more flexible but complex solutions. We recommend staying with the simplest approach
that gets the job done for your project.

1. **Built-in Bootstrap 5 Components** – The easiest way to **get started** with
   ``djangocms-frontend``. Built-in components are ready to use and require no additional
   configuration. They are perfect for quickly setting up a website with a variety of components
   that are compatible with Bootstrap 5. Pre-built components need to be explicitly
   added to your project's ``INSTALLED_APPS``.

2. **Template Components** – The easiest approach creating or porting your own
   custom components, allowing you to define them by their **HTML templates, without any code**. Special
   ``djangocms-frontend`` tags are used to provide the additional declarative information
   needed. This is the fastest approach to create ``djangocms-frontend`` components.
   Template-based (or auto) components are auto-detected.

3. **Custom Frontend Component** development – A more advanced method that lets you create
   custom components with **minimal code**. This approach is more flexible than the
   template-based method, but requires some Python coding providing more control over
   the components add and change forms, for example.

4. **Custom Plugin Development** – The most advanced option, where you create fully-fledged
   custom plugins, giving you maximum control over functionality, rendering, and
   integration with other parts of your project. This approach is the most flexible,
   but also the most complex, since template, plugin, and forms need to be created.
   For custom plugin development, see the :ref:`how-to-add-frontend-plugins` guide.

---------

**Start with one of the following tutorials:**

.. toctree::
   :maxdepth: 1

   builtin_components
   template_components
   custom_components
