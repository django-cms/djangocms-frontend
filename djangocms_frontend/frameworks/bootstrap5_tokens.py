"""Bootstrap 5 adapter for universal configuration tokens.

Tables are built once at import time. Results are immutable and safe to share.
Existing Bootstrap 5 mixins can use ``value`` at their field boundary while new
renderers use the role-aware utility and component helpers.
"""

from types import MappingProxyType

from djangocms_frontend import tokens

BREAKPOINTS = MappingProxyType({**{bp: bp for bp in tokens.BREAKPOINTS}, "2xl": "xxl"})
PROPERTIES = {v: k for k, v in tokens.PROPERTY_ALIASES.items()}
SIDES = {v: k for k, v in tokens.SIDE_ALIASES.items()}
SPACING = MappingProxyType({v: k for k, v in tokens.LEGACY_SPACING.items()})
COLORS = MappingProxyType(
    {**{c: c for c in tokens.COLORS}, "neutral-light": "light", "neutral-dark": "dark", "inverse": "dark"}
)
FIELD_VALUES = {
    field: {canonical: legacy for legacy, canonical in aliases.items()}
    for field, aliases in tokens.FIELD_ALIASES.items()
}
# Canonical semantic colours without legacy aliases also need resolution.
for _field in tokens.COLOR_FIELDS:
    FIELD_VALUES[_field] = COLORS
FIELD_VALUES["background_context"] = {
    **COLORS,
    "body": "body",
    "surface-1": "body-tertiary",
    "surface-2": "body-secondary",
}
for _field in ("card_text_color", "icon_foreground", "heading_context"):
    FIELD_VALUES[_field] = {
        **COLORS,
        "default": "body",
        "muted": "body-secondary",
        "emphasis": "body-emphasis",
        "inherit": "reset",
    }
FIELD_VALUES = MappingProxyType({field: MappingProxyType(values) for field, values in FIELD_VALUES.items()})
UNSUPPORTED_VALUES = {
    "link_size": ("xs", "xl"),
    "background_shadow": ("xs", "xl"),
    "alert_shadow": ("xs", "xl"),
    "card_type": ("horizontal",),
    "background_context": ("surface-3", "surface-4"),
    "card_text_color": ("contrast",),
    "icon_foreground": ("contrast",),
    "heading_context": ("contrast",),
    "size_x": ("dynamic-viewport", "min-content", "max-content"),
    "size_y": ("dynamic-viewport", "min-content", "max-content"),
}


# Framework choice settings listing each field's native Bootstrap 5 values.
NATIVE_CHOICE_SETTINGS = MappingProxyType(
    {
        **{field: "COLOR_STYLE_CHOICES" for field in tokens.COLOR_FIELDS},
        "alert_shadow": "SHADOW_CHOICES",
        "background_shadow": "SHADOW_CHOICES",
        "size_x": "SIZE_X_CHOICES",
        "size_y": "SIZE_Y_CHOICES",
    }
)


_native_choices = {}
_framework = None


def native_choices(field):
    """Values the project configured for ``field``, e.g. a custom theme colour."""
    global _framework
    name = NATIVE_CHOICE_SETTINGS.get(field)
    if name is None:
        return frozenset()
    if _framework is None:  # Import once and lazily: the framework imports this module.
        from djangocms_frontend.frameworks import bootstrap5 as _framework

    choices = getattr(_framework, name, ())
    cached = _native_choices.get(name)
    # Rendering calls this for every class; rebuild only if the setting was replaced.
    if cached is None or cached[0] is not choices:
        cached = _native_choices[name] = (choices, frozenset(str(choice[0]) for choice in choices))
    return cached[1]


def value(field, token):
    """Resolve canonical or legacy values for the existing Bootstrap 5 field API.

    Unrecognized project-defined values are passed through for compatibility.
    New generic renderers should use strict ``utility_classes`` instead.
    """
    if field == "space_sides":
        token = tokens.normalize_value(field, token)
    if field in tokens.SPACING_FIELDS:
        if isinstance(token, str) and token[:2] in ("ml", "mr", "pl", "pr"):
            token = tokens.normalize_value(field, token)
        if isinstance(token, dict):
            size = token["size"]
            if size in tokens.SPACING and size not in SPACING:
                raise ValueError(f"Unsupported native Bootstrap 5 spacing: {size}")
            return spacing_widget_value(token)
        return token
    if field in tokens.DEVICE_LIST_FIELDS and isinstance(token, (list, tuple)):
        return [BREAKPOINTS.get(bp, bp) for bp in token]
    if field in ("space_size", "gutters") and token in tokens.SPACING and token not in SPACING:
        raise ValueError(f"Unsupported native Bootstrap 5 spacing: {token}")
    if field in tokens.FIELD_ALIASES and token is not None and not isinstance(token, str):
        if field not in ("space_size", "gutters") or not isinstance(token, int):
            raise ValueError(f"Invalid Bootstrap 5 value: {field}={token!r}")
    # An empty link_type renders as a button (see LinkRenderMixin); it is not an error.
    if field == "link_type" and token not in ("link", "button", "btn", "", None):
        raise ValueError(f"Invalid Bootstrap 5 link type: {token!r}")
    if isinstance(token, str):
        # A project's own native value (e.g. a theme colour "accent" or a shadow "md")
        # may share a universal token's name. It is native here, so it wins over any
        # token mapping and is passed through unchanged.
        if token in native_choices(field):
            return token
        if token in UNSUPPORTED_VALUES.get(field, ()) or (field in tokens.COLOR_FIELDS and token == "accent"):
            raise ValueError(f"Unsupported native Bootstrap 5 value: {field}={token}")
        return FIELD_VALUES.get(field, {}).get(token, token)
    return token


def spacing_widget_value(token):
    """Represent stored spacing in the editor, including a non-native size.

    This is an editing representation only; ``value`` still rejects unsupported
    sizes for rendering and migration validation.
    """
    return f"{PROPERTIES[token['property']]}{SIDES[token['side']]}-{SPACING.get(token['size'], token['size'])}"


def config_values(config):
    """Project a canonical config onto legacy form field names without changing it."""
    result = {}
    for key, token in config.items():
        name = tokens.legacy_key(key)
        result[name] = value(name, token)
    return result


def field_value(instance, field, default=""):
    """Resolve a presentation value, omitting unsupported styles during rendering.

    ``value`` remains strict for forms and migration diagnostics. Rendering must
    not turn an unsupported stored option into a page error.
    """
    if instance is None or not hasattr(instance, "config"):
        return default
    try:
        token = getattr(instance, field, instance.config.get(field, default))
        # A field the plugin's project form declares itself holds the project's own value.
        if field in _project_fields(instance):
            return token
        return value(field, token)
    except (ValueError, KeyError, TypeError):
        return default


_plugin_project_fields = None


def _project_fields(instance):
    """The project fields of the instance's plugin form, resolved once per instance:
    rendering asks for every field value."""
    global _plugin_project_fields
    plugin_type = getattr(instance, "plugin_type", None)
    if not plugin_type:
        return frozenset()
    cached = vars(instance).get("_token_project_fields")
    if cached is not None and cached[0] == plugin_type:
        return cached[1]
    if _plugin_project_fields is None:  # Import once and lazily: token_forms needs settings.
        from djangocms_frontend.token_forms import plugin_project_fields as _plugin_project_fields

    fields = _plugin_project_fields(plugin_type)
    try:
        instance._token_project_fields = (plugin_type, fields)
    except AttributeError:  # e.g. an object with __slots__
        pass
    return fields


def grid_value(instance, field):
    # UI field names remain stable during the storage rollout.
    return instance.config.get(tokens.canonical_key(field), instance.config.get(field))


def _responsive(stem, suffix, breakpoint):
    bp = BREAKPOINTS[breakpoint]
    return f"{stem}-{suffix}" if bp == "xs" else f"{stem}-{bp}-{suffix}"


_maps = {}
for _bp in tokens.BREAKPOINTS:
    for _role, _stem in {
        "margin": "m",
        "margin-top": "mt",
        "margin-bottom": "mb",
        "margin-start": "ms",
        "margin-end": "me",
        "margin-horizontal": "mx",
        "margin-vertical": "my",
        "padding": "p",
        "padding-top": "pt",
        "padding-bottom": "pb",
        "padding-start": "ps",
        "padding-end": "pe",
        "padding-horizontal": "px",
        "padding-vertical": "py",
        "gutter": "g",
    }.items():
        for _token, _step in SPACING.items():
            _maps[(_role, _token, _bp)] = (_responsive(_stem, _step, _bp),)
        if _role.startswith("margin"):
            _maps[(_role, "auto", _bp)] = (_responsive(_stem, "auto", _bp),)
    for _display in ("none", "block", "inline", "inline-block", "flex", "inline-flex", "grid"):
        _maps[("display", _display, _bp)] = (_responsive("d", _display, _bp),)

for _color, _native in COLORS.items():
    if _color == "accent":  # Requires a project palette; stock Bootstrap 5 has no accent.
        continue
    for _role, _prefix in (("foreground", "text"), ("background", "bg"), ("border", "border")):
        _maps[(_role, _color, "xs")] = (f"{_prefix}-{_native}",)
for _surface, _cls in {
    "body": "bg-body",
    "surface-1": "bg-body-tertiary",
    "surface-2": "bg-body-secondary",
    "white": "bg-white",
    "black": "bg-black",
    "transparent": "bg-transparent",
}.items():
    _maps[("surface", _surface, "xs")] = (_cls,)
for _token, _cls in {
    "default": "text-body",
    "muted": "text-body-secondary",
    "emphasis": "text-body-emphasis",
    "inherit": "text-reset",
    "white": "text-white",
    "black": "text-black",
}.items():
    _maps[("foreground", _token, "xs")] = (_cls,)
for _token, _cls in {"none": "shadow-none", "sm": "shadow-sm", "md": "shadow", "lg": "shadow-lg"}.items():
    _maps[("shadow", _token, "xs")] = (_cls,)
for _token, _cls in {
    "rem-0": "rounded-0",
    "rem-0.25": "rounded-1",
    "rem-0.375": "rounded-2",
    "rem-0.5": "rounded-3",
    "rem-1": "rounded-4",
    "rem-2": "rounded-5",
    "pill": "rounded-pill",
    "circle": "rounded-circle",
}.items():
    _maps[("radius", _token, "xs")] = (_cls,)
# Larger stock font-size utilities use RFS and do not have a fixed rem contract.
for _token, _step in {"rem-1": "6", "rem-1.25": "5"}.items():
    _maps[("font-size", _token, "xs")] = (f"fs-{_step}",)

for _percent in (0, 10, 25, 50, 75, 100):
    # Bootstrap background opacity omits zero in the standard utility build.
    if _percent:
        _maps[("background-opacity", _percent, "xs")] = (f"bg-opacity-{_percent}",)
for _role, _prefix in (
    ("text-alignment", "text"),
    ("items-alignment", "align-items"),
    ("self-alignment", "align-self"),
    ("distribution", "justify-content"),
):
    _values = ("start", "center", "end")
    if _role in ("items-alignment", "self-alignment"):
        _values += ("stretch", "baseline")
    if _role == "distribution":
        _values += ("between", "around", "evenly")
    for _token in _values:
        _maps[(_role, _token, "xs")] = (f"{_prefix}-{_token}",)
for _axis, _stem in (("width", "w"), ("height", "h")):
    for _n in (25, 50, 75, 100):
        _maps[(_axis, f"percent-{_n}", "xs")] = (f"{_stem}-{_n}",)
    _maps[(_axis, "auto", "xs")] = (f"{_stem}-auto",)
_maps[("width", "viewport", "xs")] = ("vw-100",)
_maps[("height", "viewport", "xs")] = ("vh-100",)
_maps[("min-height", "viewport", "xs")] = ("min-vh-100",)
UTILITIES = MappingProxyType(_maps)
del _maps


def utility_classes(role, token, *, breakpoint="xs"):
    """Return a supported native recipe or fail explicitly; never silently approximate."""
    try:
        return UTILITIES[(role, token, breakpoint)]
    except (KeyError, TypeError) as exc:
        raise ValueError(f"Unsupported Bootstrap 5 utility: {role}={token!r} at {breakpoint}") from exc


_COMPONENTS = {
    "button": {
        "base": ("btn",),
        "colors": tuple(c for c in COLORS if c != "accent"),
        "variants": ("solid", "outline", "link"),
        "sizes": ("sm", "md", "lg"),
    },
    "alert": {"base": ("alert",), "colors": tuple(c for c in COLORS if c != "accent"), "variants": ("solid",)},
    "badge": {"base": ("badge",), "colors": tuple(c for c in COLORS if c != "accent"), "variants": ("solid",)},
    "list-item": {
        "base": ("list-group-item",),
        "colors": tuple(c for c in COLORS if c != "accent"),
        "variants": ("solid",),
    },
}
_COMPONENT_COLORS = {}
for _component, _options in _COMPONENTS.items():
    for _color in _options["colors"]:
        for _variant in _options["variants"]:
            _native = COLORS[_color]
            if _component == "button":
                _cls = (
                    "btn-link" if _variant == "link" else f"btn-{'outline-' if _variant == 'outline' else ''}{_native}"
                )
            else:
                _prefix = {"alert": "alert", "badge": "bg", "list-item": "list-group-item"}[_component]
                _cls = f"{_prefix}-{_native}"
            _COMPONENT_COLORS[(_component, _color, _variant)] = (_cls,)
_COMPONENT_COLORS = MappingProxyType(_COMPONENT_COLORS)


def supported_options(component):
    options = _COMPONENTS[component]
    return {key: val for key, val in options.items() if key != "base"}


def component_classes(component, *, color="primary", variant="solid", size="md"):
    options = _COMPONENTS.get(component)
    if options is None or size not in options.get("sizes", ("md",)):
        raise ValueError(f"Unsupported Bootstrap 5 component or size: {component}/{size}")
    try:
        classes = options["base"] + _COMPONENT_COLORS[(component, color, variant)]
    except KeyError as exc:
        raise ValueError(f"Unsupported Bootstrap 5 component options: {component}/{color}/{variant}") from exc
    if component == "button" and size != "md":
        classes += (f"btn-{size}",)
    return classes


def iter_class_names():
    names = {name for recipe in UTILITIES.values() for name in recipe}
    names.update(name for recipe in _COMPONENT_COLORS.values() for name in recipe)
    names.update(name for options in _COMPONENTS.values() for name in options["base"])
    names.update(("btn-sm", "btn-lg"))
    return iter(sorted(names))
