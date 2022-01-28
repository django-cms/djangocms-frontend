How-to guides
#############

How to extend existing plugins
******************************

Existing plugins can be extended through two type of
class mixins. ``djangocms-frontend`` looks for these mixins
in two places:

1. In the theme module. Its name is specified by the setting ``DJANGOCMS_FRONTEND_THEME``
   and defaults to ``djangocms_frontend``.

2. In djangocms_frontend.contrib.*app*.frontends.*framework*.py.

Both mixins are included and all methods have to call the super methods
to ensure all form extensions and render functionalities are processed.

The theme module is primarily thought to allow for third party
extensions in terms of functionality and/or design.

The framework module is primarily thought to allow for adaptation of
``djangocms-frontend`` to other css frameworks besides Bootstrap 5.


RenderMixins
============

The render mixins are called "*PluginName*RenderMixin" and are applied
to the plugin class. This allows for the redefinition of the ``CMSPlugin.render``
method, especially to prepare the context for rendering.

In addition it allows the definition of ``CMSPlugin.get_fieldsets`` it
allows for extension or change of the plugin's admin form. The admin form
is used to edit or create a plugin.

FormMixins
==========

Form mixins are used to add fields to a plugin's admin form.
These fields are available to the render mixins and, of course,
to the plugin templates.

Working example
===============

Let's say you wanted to extend the ``GridContainerPlugin`` to
offer the option for a background color, a background image,
some transparency and say a blur effect.


How to create a theme app
*************************
``djangocms-frontend`` is designed to be "themable".
A theme typically will do one or more of the following:

* Style the appearance using css

* Extend standard plugins

* Add custom plugins



How to add support for a new css framework
******************************************
