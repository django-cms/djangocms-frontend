################
Universal tokens
################

.. versionadded:: 3.0

Universal tokens describe a plugin's design independently of the CSS framework
that renders it. Configuration stores ``button``, ``sm``, and ``rem-1``; the
Bootstrap 5 adapter translates these into the appropriate classes and markup.
This separates stored content from framework class names and ordinal scales.
See :doc:`frameworks` for how framework selection, renderers, templates, and
assets fit together.

Bootstrap 5 is the first implemented adapter. The vocabulary provides an
extension point for other frameworks; it does not itself add Bootstrap 6,
Foundation, or Tailwind rendering.

Storage and compatibility
=========================

Canonical configuration includes ``"_frontend_tokens": 1``. Untagged legacy
Bootstrap 5 configuration remains readable. Normalization accepts a mixture of
legacy and canonical fields, is idempotent, and rejects unknown schema versions
or conflicting legacy/canonical grid keys. Rendering never rewrites stored JSON.
When model or project defaults contain both spellings of a grid key, the canonical
key takes precedence and a warning identifies the conflict. Forms do the same for
stored configuration: they show and keep the canonical key's value, also for fields
that are disabled or not on the form, so a conflict never blocks a save. Unknown
schema versions still fail form validation. Migration validation remains strict
about conflicting stored values.

For example, legacy Bootstrap 5 configuration::

    {
        "link_type": "btn",
        "link_size": "btn-sm",
        "margin_x": "mx-3",
        "margin_devices": ["xs", "xxl"]
    }

becomes::

    {
        "_frontend_tokens": 1,
        "link_type": "button",
        "link_size": "sm",
        "margin_x": {
            "property": "margin",
            "side": "horizontal",
            "size": "rem-1"
        },
        "margin_devices": ["xs", "2xl"]
    }

Both configurations render the same Bootstrap 5 spacing and breakpoint classes.
The structured spacing value separates property, side, and physical size.
Legacy strings with no selected size, such as ``mx-``, normalize to an empty
setting and do not block migration. An absent or empty setting means no explicit rule; ``rem-0`` means an explicit
zero, including responsive resets.

Built-in forms and the default component form base normalize configuration on
successful validation. ``initialize_from_form`` also canonicalizes defaults
and existing configuration. Adapter widgets retain their existing Bootstrap 5 values
and names, so breakpoint icons and existing admin integrations continue working.
A migrated record is projected back to those widget values when edited, then
stored canonically again. Unchanged widget selections preserve the original universal
role when several roles share a native recipe. A newly selected unsupported token
produces a form validation error; a stored one is offered by its widget and kept
when posted back unchanged. Strict validation covers editable fields on the form;
unsupported stored options outside that form or in disabled fields are preserved
without blocking an unrelated edit. Submitted values for disabled fields are ignored. Editors can replace or clear unsupported tokens where fields
are available. Custom forms should inherit
``djangocms_frontend.token_forms.EntangledModelForm`` to use this boundary.
Existing code that writes legacy JSON directly continues to work; canonicalizing
such writes explicitly avoids leaving a mixture of formats in storage.

Fields declared by project forms keep their own values and names, even when
they share a built-in token name. This exclusion applies to forms, initialization,
the plugin template tag, and migration. Explicit form initials take precedence
over stored values in both native and canonical spelling.

Stored spacing sizes unavailable in Bootstrap remain visible in the spacing
controls. An unchanged save preserves them; choosing a supported size replaces
them, and clearing the size removes the setting.

Only recognized top-level option fields are translated. Relation dictionaries,
HTML attributes, custom classes, rich text, and unrelated extension JSON are
preserved. Custom templates and code that previously compared configuration
against Bootstrap class names must use canonical tokens or the adapter helper.

The vocabulary
==============

A token's meaning belongs to its role. Component size ``sm`` and shadow ``sm``
are separate scales. Heading level remains HTML structure rather than a font
size. Colour mode is independent of background colour.

.. list-table:: Core domains
   :header-rows: 1
   :widths: 25 75

   * - Domain
     - Tokens
   * - Breakpoints
     - ``xs``, ``sm``, ``md``, ``lg``, ``xl``, ``2xl``
   * - Theme colours
     - ``primary``, ``secondary``, ``accent``, ``success``, ``info``,
       ``warning``, ``danger``, ``inverse``, ``neutral-light``, ``neutral-dark``
   * - Surfaces
     - ``body``, ``surface-1`` through ``surface-4``, ``white``, ``black``, ``transparent``
   * - Foregrounds
     - Theme colours, ``default``, ``muted``, ``emphasis``, ``contrast``,
       ``inherit``, ``white``, ``black``
   * - Component variants
     - ``solid``, ``outline``, ``subtle``, ``text``, ``link``
   * - Component sizes
     - ``xs``, ``sm``, ``md``, ``lg``, ``xl``
   * - Shadows
     - ``none``, ``xs``, ``sm``, ``md``, ``lg``, ``xl``
   * - Sides
     - ``all``, ``top``, ``bottom``, ``start``, ``end``, ``horizontal``, ``vertical``

These domains are the shared vocabulary, not a promise that every adapter or
existing plugin field supports every value. The first Bootstrap 5 implementation
exposes native recipes without approximating missing sizes or colours.
For example, stock Bootstrap 5 has no native spacing step for ``rem-0.75`` and
no ``accent`` component colour; strict resolution rejects those requests.
The field adapter also rejects ``accent`` in colour fields: forms report a field
error, migration reports the record as unmapped, and rendering omits that colour.
No extra frontend stylesheet is required for the supported native subset.
Adaptive surface and foreground helpers target Bootstrap 5.3; projects using
older Bootstrap 5 assets should use only the options present in those assets.

Legacy ``light`` and ``dark`` colour contexts become ``neutral-light`` and
``neutral-dark``. These preserve their Bootstrap 5 palette entries rather than
changing them into adaptive surfaces or pure white/black. ``navbar_design``
retains ``light``/``dark`` because it represents colour mode. Another adapter
must provide explicit equivalents or declare these fixed neutral roles
unsupported. ``inverse`` maps to the Bootstrap 5 dark palette entry.

Spacing uses a finite physical scale:

.. list-table:: Spacing conversion
   :header-rows: 1

   * - Universal token
     - Reference size
     - Bootstrap 5 step
   * - ``rem-0``
     - 0
     - ``0``
   * - ``rem-0.25``
     - .25rem
     - ``1``
   * - ``rem-0.5``
     - .5rem
     - ``2``
   * - ``rem-0.75``
     - .75rem
     - Unsupported natively
   * - ``rem-1``
     - 1rem
     - ``3``
   * - ``rem-1.25``
     - 1.25rem
     - Unsupported natively
   * - ``rem-1.5``
     - 1.5rem
     - ``4``
   * - ``rem-2``
     - 2rem
     - Unsupported natively
   * - ``rem-2.5``
     - 2.5rem
     - Unsupported natively
   * - ``rem-3``
     - 3rem
     - ``5``

Legacy spacing sides ``l`` and ``r`` are accepted as aliases for ``start`` and
``end`` and render using Bootstrap 5's ``s`` and ``e`` utilities.

``auto`` is available for margins, never padding or gutters. Reference sizes
assume the standard Bootstrap 5 scale; projects using customized spacing Sass
must reconcile their scale before conversion. Custom ordinal values are
reported by the migration rather than guessed.

Radius and font-size tokens also use explicit rem values. Radius additionally
supports ``pill`` and ``circle``. Opacity is a percentage rather than a framework
step; background opacity is stored as an integer percentage. Sizing uses ``percent-25``, ``percent-50``, ``percent-75``, ``percent-100``,
``auto``, and explicit viewport/content modes. In particular, legacy
``min-vh-100`` becomes ``min-viewport`` in ``size_y``: conversion preserves a
minimum height rather than changing it into a fixed height.

Class-valued component options become semantic values:

.. list-table:: Component conversions
   :header-rows: 1

   * - Option
     - Legacy value
     - Universal value
   * - Container
     - ``container``, ``container-fluid``, ``container-full``
     - ``bounded``, ``fluid``, ``full``
   * - Card layout
     - ``card-group``, ``row``
     - ``group``, ``grid``
   * - Card section
     - ``card-header``, ``card-body``, ``card-footer``, ``card-img-overlay``
     - ``header``, ``body``, ``footer``, ``image-overlay``
   * - Tabs
     - ``nav-tabs``, ``nav-pills``
     - ``tabs``, ``pills``
   * - Tabs alignment
     - ``nav-fill``, ``nav-justified``, ``flex-column``
     - ``fill``, ``justified``, ``vertical``
   * - Button
     - ``btn``, ``btn-sm``, ``btn-lg``
     - ``button``, ``sm``, ``lg``
   * - Carousel transition
     - Empty string, ``carousel-fade``
     - ``slide``, ``fade``
   * - Alignment
     - ``align-items-center``, ``justify-content-between``, ``align-self-end``
     - ``center``, ``between``, ``end`` in their respective fields

Existing independent booleans, numeric grid values, and plugin field names stay
in place. For example, ``link_outline`` remains a boolean; the generic component
API additionally accepts ``variant="outline"``. New options are not added to
existing plugins solely because the vocabulary defines them.

The Bootstrap 5 adapter retains the existing ``container-full`` class for
``full``; projects supplying its CSS retain control over that layout. Its
meaning is not silently replaced with Bootstrap's padded fluid container.
Grid numeric semantics are preserved, including zero representing a
content-sized column and the base ``col`` providing equal-share layout.

Breakpoint tokens express ordered levels. Bootstrap 5 rendering retains its
existing breakpoint widths and emits ``xxl`` in CSS while storing ``2xl`` in
configuration, including ``2xl_col`` and ``row_cols_2xl``. A future adapter must
specify its breakpoint profile before a framework switch can preserve layout
thresholds.

Rendering and performance
=========================

The existing framework module is selected once when settings are imported.
Bootstrap 5 exports its adapter as ``settings.token_adapter``. The adapter
prepares immutable utility tables at import time; resolving a supported utility
is one dictionary lookup returning an immutable tuple::

    from djangocms_frontend import settings

    settings.token_adapter.utility_classes(
        "padding-top", "rem-1", breakpoint="md"
    )
    # ("pt-md-3",)

    settings.token_adapter.component_classes(
        "button", color="danger", variant="outline", size="sm"
    )
    # ("btn", "btn-outline-danger", "btn-sm")

Component rendering combines precomputed base and colour/variant fragments with
a size fragment. It does not precompute every possible configuration combination.
``supported_options(component)`` exposes supported component choices, and
``iter_class_names()`` enumerates classes owned by these generic recipes. It
does not enumerate every existing plugin template or arbitrary project class.

Existing Bootstrap 5 mixins use ``field_value(instance, field, default)`` to
translate only the fields they consume. The compatibility projection accepts
legacy and canonical values. Presentation resolution skips unsupported styles,
allowing the rest of the plugin and page to render. Strict resolution remains
available through ``value`` and the generic recipe helpers for form validation
and migration diagnostics. Framework-specific templates can load
``frontend_tokens`` and use ``instance|framework_value:"tab_type"`` when they
need a class-valued option. The ``parent_framework_value`` tag resolves parent
options directly, so card layout wrappers do not depend on a particular render
mixin populating context. Storage must not contain resolved class tuples.

Token rendering adds no database queries, framework imports per token, CSS
compilation, or network requests. Legacy parsing belongs to normalization and
form/migration boundaries. Canonical spacing is already structured, so the
renderer does not parse physical token strings into numbers.

A second cache around a dictionary lookup is unnecessary. Any future cache of
expensive component recipes should be bounded and include the asset/profile
revision and all relevant presentation inputs. Tables are rebuilt on worker
restart after settings or theme changes. Existing page/fragment caches remain
separate from token lookup.

Template plugin arguments also accept legacy and canonical breakpoint keys; both
spellings override the same canonical default.

The tests verify output parity and zero database queries for token resolution.
End-to-end latency still needs measurement on representative uncached pages;
no percentage speedup or overhead guarantee is implied by the lookup design.

Migrating stored content
========================

Back up the database and review custom templates/settings that consume raw
configuration. Preview the conversion::

    python manage.py frontend migrate --from bootstrap5 --to universal --dry-run

Apply it::

    python manage.py frontend migrate --from bootstrap5 --to universal

Add ``--fail-on-unmapped`` to roll back the entire invocation if any record
cannot be converted. Otherwise, unmapped records are reported with their model
and primary key and left unchanged while supported records are converted.
``--database ALIAS`` selects the database; the default is ``default``.

Conversion requires ``DJANGOCMS_FRONTEND_FRAMEWORK = "bootstrap5"``. Other active
frameworks are rejected before any data is written.

The command scans every row in each installed concrete frontend configuration
table, including published/draft/archived content represented by those rows and
custom models based on ``AbstractFrontendUIItem``. Proxy models are visited via
their concrete table. External revision snapshots or serialized exports are not
rewritten. Unknown nested extension data remains untouched. Fields declared by
the registered plugin's project form are excluded from token conversion, including
fields whose names collide with built-in token fields.

Conversion runs in a transaction. Oracle locks rows with ``select_for_update``
while reading and updating them, avoiding equality comparisons on JSON LOBs.
Other backends check the original stored JSON representation before updating,
so concurrent changes cause rollback. On SQLite the comparison uses the exact
stored text, preserving compatibility with existing whitespace and key order.
Conversion uses direct updates rather than model save hooks. Running it again skips unchanged records.
There is no automatic database schema migration and no reverse-conversion
command; restore the backup if a full rollback is required. Clear project/CMS
rendered-content caches after deployment and conversion, especially when custom
templates consume canonical configuration directly. Unqualified
``frontend migrate`` continues to run the existing third-party plugin migration.
