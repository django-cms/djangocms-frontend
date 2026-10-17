##########
Frameworks
##########

A framework integration translates frontend plugins into the HTML, CSS classes,
and interactions expected by a particular CSS framework. Plugins describe
content and layout; the integration supplies their presentation. Bootstrap 5
is the complete built-in integration and the default rendering target.

A working integration needs more than a class-name mapping. Its forms,
responsive rules, component templates, CSS, and JavaScript must agree about
what a saved option means.

Framework selection
===================

The project selects its framework with a Django setting::

    DJANGOCMS_FRONTEND_FRAMEWORK = "bootstrap5"

``djangocms-frontend`` imports framework settings from
``djangocms_frontend.frameworks.<framework>``. That module defines choices and
metadata used throughout the plugin suite, including devices, spacing, colours,
sizing, navigation options, and links to framework documentation.

Selection happens when settings and plugin modules are imported. Treat a
framework change as a deployment configuration change and restart application
workers. It is not a per-request theme switch.

The setting selects an existing integration; assigning another framework name
does not generate one. Bootstrap 6, Foundation, and Tailwind require complete
integrations before they can render the plugin suite. Partial Foundation mixins
and the Tailwind settings module in the source tree do not establish equivalent
support.

What an integration owns
========================

.. list-table:: Framework responsibilities
   :header-rows: 1
   :widths: 25 75

   * - Part
     - Responsibility
   * - Settings
     - Define available choices, device names, and plugin metadata.
   * - Common mixins
     - Render shared background, spacing, sizing, and visibility options, and
       provide the corresponding form fields.
   * - Plugin mixins
     - Apply component-specific classes and rendering context, and select
       templates where needed.
   * - Templates
     - Supply the component's HTML structure, accessibility attributes, and
       interaction hooks.
   * - Token adapter
     - Translate universal configuration values into supported framework recipes
       and bridge existing form widget values.
   * - Assets
     - Supply CSS and JavaScript matching those recipes and templates.

Common mixins are loaded from
``djangocms_frontend.common.<framework>``. Individual plugin groups provide
framework mixins under their own package, for example
``djangocms_frontend.contrib.grid.frameworks.bootstrap5``.

Template paths commonly include the framework name, such as
``djangocms_frontend/bootstrap5/grid_row.html``. Plugins with selectable template
sets use paths such as
``djangocms_frontend/bootstrap5/link/default/link.html``. Some render mixins
specify a template directly; others let the plugin select one. The template-set
helper falls back to that framework's ``default`` variant when the requested
variant is missing, rather than selecting a different framework.

Frameworks and universal tokens
===============================

.. versionadded:: 3.0
   Universal configuration tokens and the Bootstrap 5 token adapter.

Universal tokens are the storage vocabulary shared by integrations. A spacing
value such as ``rem-1`` describes a reference size; the Bootstrap 5 adapter can
render it as spacing step ``3``. Configuration does not need to store the class
``pt-md-3`` to express padding at a particular breakpoint.

The selected framework settings module can export ``token_adapter``. The
Bootstrap 5 integration exposes utility and component recipes through this
adapter, while its existing render mixins use compatibility helpers to accept
both legacy and canonical configuration. Built-in forms translate their widget
values at the storage boundary.

Tokens preserve intent; adapters determine whether and how that intent can be
rendered. A shared token does not guarantee native support in every framework.
The Bootstrap 5 adapter rejects unsupported generic recipes instead of silently
rounding sizes or choosing another colour. Existing project-specific values
retain a compatibility path, and the migration command reports configurations
it cannot convert safely.

See :doc:`universal-tokens` for the vocabulary, adapter interface, storage
version, performance design, and Bootstrap 5 conversion command.

Templates and interaction
=========================

Two frameworks may require different HTML for the same plugin. A disclosure
component can use buttons and collapsible panels in one integration and native
``details`` elements in another. A menu may require different wrappers,
attributes, and keyboard handling. Those differences belong in framework
renderers, templates, and interaction code.

Changing CSS classes alone cannot adapt a component whose markup or behaviour
has changed. The integration must preserve the plugin's content, configured
state, accessibility, and behaviour in both normal rendering and CMS editing or
preview.

The project must load compatible frontend assets in its page templates. The
framework setting does not install dependencies, rebuild stylesheets, or make
arbitrary project templates include the required assets. Project Sass overrides
and custom builds must agree with the adapter's spacing scale, palette, utility
classes, and breakpoint thresholds.

Frameworks and project themes
============================

A framework integration supplies the rendering rules. A project theme customizes
the site's appearance and can extend those rules without changing the storage
vocabulary.

``DJANGOCMS_FRONTEND_THEME`` identifies the theme package; its default is
``djangocms_frontend``. The mixin loader looks for theme rendering mixins in
``<theme>.frameworks.<framework>`` and theme form mixins in ``<theme>.forms``.
Matching theme mixins precede the built-in framework mixins in the generated
class hierarchy, allowing cooperative overrides using ``super()``.

Template overrides use Django's normal template loading mechanism. Keeping a
Bootstrap 5 integration while overriding a card template is a theme change;
implementing another framework's component structure and interaction model is a
framework integration.

See :doc:`../how-to/create-themes` and
:doc:`../how-to/extend-frontend-plugins` for customization guidance.

Changing frameworks
===================

Universal storage reduces the amount of data tied to Bootstrap class names,
but a framework change still requires compatible rendering and assets. Review
saved options against the target integration's capabilities and breakpoint
profile, including project overrides and custom templates that read raw
configuration.

The same breakpoint name can represent different widths in different
integrations. Likewise, a colour role can resolve to a different palette.
Preserving responsive thresholds or exact appearance requires an explicit
mapping and matching compiled assets; it does not follow from retaining the
token names.

Converting Bootstrap 5 configuration to universal tokens keeps Bootstrap 5 as
the rendering framework. It prepares stored values for independent adapters;
it does not switch the site's framework or convert its project templates.
