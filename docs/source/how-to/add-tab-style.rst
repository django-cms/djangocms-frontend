How to add the tab editing style to your custom plugins
=======================================================

If you prefer the tabbed frontend editing style of ``djangocms-frontend`` you can easily
add it to your own plugins.

If you use the standard editing form, just add a line specifying the
``change_form_template`` to your plugin class:

.. code-block:: python

    class MyCoolPlugin(CMSPluginBase):
        ...
        change_form_template = "djangocms_frontend/admin/base.html"
        ...

If you already have your own ``change_form_template``, make sure it extends
``djangocms_frontend/admin/base.html``:

.. code-block::

    {% extends "djangocms_frontend/admin/base.html" %}
    {% block ...%}
        ...
    {% endblock %}
