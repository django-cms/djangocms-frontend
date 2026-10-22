"""Framework-independent configuration values and Bootstrap 5 legacy normalization.

No Django imports: migration tools, asset generators, and adapters share this contract.
"""

import sys

VERSION_KEY = "_frontend_tokens"
VERSION = 1
BREAKPOINTS = ("xs", "sm", "md", "lg", "xl", "2xl")
SPACING = ("rem-0", "rem-0.25", "rem-0.5", "rem-0.75", "rem-1", "rem-1.25", "rem-1.5", "rem-2", "rem-2.5", "rem-3")
LEGACY_SPACING = dict(
    zip(("0", "1", "2", "3", "4", "5"), ("rem-0", "rem-0.25", "rem-0.5", "rem-1", "rem-1.5", "rem-3"))
)
COLORS = (
    "primary",
    "secondary",
    "accent",
    "success",
    "info",
    "warning",
    "danger",
    "inverse",
    "neutral-light",
    "neutral-dark",
)
SURFACES = ("body", "surface-1", "surface-2", "surface-3", "surface-4", "white", "black", "transparent")
FOREGROUNDS = ("default", "muted", "emphasis", "contrast", "inherit", "white", "black") + COLORS
VARIANTS = ("solid", "outline", "subtle", "text", "link")
COLOR_MODES = ("inherit", "light", "dark", "auto")
ALIGNMENT = ("start", "center", "end", "stretch", "baseline")
DISTRIBUTION = ("start", "center", "end", "between", "around", "evenly")
DISPLAY = ("none", "block", "inline", "inline-block", "flex", "inline-flex", "grid", "flow-root", "contents")
OPACITY = tuple(range(101))
COMPONENT_SIZES = ("xs", "sm", "md", "lg", "xl")
SHADOWS = ("none", "xs", "sm", "md", "lg", "xl")
RADII = ("rem-0", "rem-0.25", "rem-0.375", "rem-0.5", "rem-1", "rem-1.5", "rem-2", "pill", "circle")
FONT_SIZES = (
    "rem-0.75",
    "rem-0.875",
    "rem-1",
    "rem-1.25",
    "rem-1.5",
    "rem-1.75",
    "rem-2",
    "rem-2.5",
    "rem-3",
    "rem-5",
)
SIDES = ("all", "top", "bottom", "start", "end", "horizontal", "vertical")
SIDE_ALIASES = {
    "r": "end",
    "l": "start",
    "": "all",
    "t": "top",
    "b": "bottom",
    "s": "start",
    "e": "end",
    "x": "horizontal",
    "y": "vertical",
}
PROPERTY_ALIASES = {"m": "margin", "p": "padding"}
COLOR_ALIASES = {"light": "neutral-light", "dark": "neutral-dark"}
SPACING_FIELDS = ("margin_x", "margin_y", "padding_x", "padding_y")
DEVICE_LIST_FIELDS = ("margin_devices", "padding_devices", "responsive_visibility")
COLOR_FIELDS = (
    "alert_context",
    "badge_context",
    "background_context",
    "card_text_color",
    "card_outline",
    "link_context",
    "list_context",
    "icon_foreground",
    "heading_context",
)

# Per-field aliases avoid interpreting the same string in unrelated extension data.
FIELD_ALIASES = {
    "container_type": {"container": "bounded", "container-fluid": "fluid", "container-full": "full"},
    "vertical_alignment": {f"align-items-{x}": x for x in ("start", "center", "end", "stretch", "baseline")},
    "horizontal_alignment": {
        f"justify-content-{x}": x for x in ("start", "center", "end", "between", "around", "evenly")
    },
    "column_alignment": {f"align-self-{x}": x for x in ("start", "center", "end", "stretch", "baseline")},
    "card_type": {"card-group": "group", "row": "grid"},
    "inner_type": {
        "card-body": "body",
        "card-header": "header",
        "card-footer": "footer",
        "card-img-overlay": "image-overlay",
    },
    "tab_type": {"nav-tabs": "tabs", "nav-pills": "pills", "nav-underline": "underline"},
    "tab_alignment": {
        "nav-fill": "fill",
        "nav-justified": "justified",
        "flex-column": "vertical",
        **{f"justify-content-{x}": x for x in ("start", "center", "end")},
    },
    "link_type": {"btn": "button"},
    "link_size": {"": "md", "btn-sm": "sm", "btn-lg": "lg"},
    "carousel_transition": {"": "slide", "carousel-fade": "fade"},
    "background_shadow": {"reg": "md"},
    "alert_shadow": {"reg": "md"},
    "space_property": PROPERTY_ALIASES,
    "space_sides": SIDE_ALIASES,
    "space_size": LEGACY_SPACING,
    "gutters": LEGACY_SPACING,
    "space_device": {"xxl": "2xl"},
    "navbar_breakpoint": {"xxl": "2xl"},
    "size_x": {**{str(n): f"percent-{n}" for n in (25, 50, 75, 100)}, "vw-100": "viewport"},
    # Preserve the legacy *minimum* height rather than converting it to a fixed height.
    "size_y": {
        **{str(n): f"percent-{n}" for n in (25, 50, 75, 100)},
        "vh-100": "viewport",
        "min-vh-100": "min-viewport",
    },
    **{field: COLOR_ALIASES for field in COLOR_FIELDS},
}


def normalize_value(field, value):
    """Normalize one legacy field; canonical and project-specific values survive unchanged."""
    if field in SPACING_FIELDS and value:
        if isinstance(value, dict):
            return "" if set(value) == {"property", "side", "size"} and value.get("size") == "" else value
        if isinstance(value, str) and "-" in value:
            prefix, size = value.split("-", 1)
            if prefix and prefix[0] in PROPERTY_ALIASES and prefix[1:] in SIDE_ALIASES:
                if not size:
                    return ""
                return {
                    "property": PROPERTY_ALIASES[prefix[0]],
                    "side": SIDE_ALIASES[prefix[1:]],
                    "size": LEGACY_SPACING.get(size, size),
                }
        return value
    if field in DEVICE_LIST_FIELDS and isinstance(value, (list, tuple)):
        return ["2xl" if bp == "xxl" else bp for bp in value]
    if field == "background_opacity" and isinstance(value, str) and value.isdecimal():
        return int(value)
    if isinstance(value, str):
        target = FIELD_ALIASES.get(field, {}).get(value, value)
        # If the project configured the target as a native value of its own (e.g. shadows
        # "reg" and "md"), converting would turn one project choice into the other.
        if target != value and target in _native_choices(field):
            return value
        return target
    return value


def _native_choices(field):
    # Consult a running project's adapter without importing or configuring Django.
    # Standalone converters use the stock vocabulary until settings are loaded.
    settings = sys.modules.get("djangocms_frontend.settings")
    adapter = getattr(settings, "token_adapter", None)
    native_choices = getattr(adapter, "native_choices", None)
    return native_choices(field) if native_choices is not None else ()


GRID_KEY_ALIASES = {
    "row_cols_xxl": "row_cols_2xl",
    **{f"xxl_{field}": f"2xl_{field}" for field in ("col", "order", "offset", "ms", "me")},
}
LEGACY_GRID_KEYS = {canonical: legacy for legacy, canonical in GRID_KEY_ALIASES.items()}


def canonical_key(key):
    return GRID_KEY_ALIASES.get(key, key)


def legacy_key(key):
    return LEGACY_GRID_KEYS.get(key, key)


def same_value(a, b):
    """Grid values are posted as strings but stored as integers: "6" and 6 agree."""
    return a == b or (not isinstance(a, (dict, list)) and str(a) == str(b))


def resolve_aliases(config, *, skip=()):
    """Return a copy in which canonical grid keys shadow their legacy aliases.

    Also returns the canonical keys whose two spellings held different values.
    Project-owned keys in ``skip`` are never treated as aliases.
    """
    if not isinstance(config, dict):
        return config, []
    config = dict(config)
    conflicts = []
    for legacy, canonical in GRID_KEY_ALIASES.items():
        if legacy in skip or canonical in skip:
            continue
        if legacy in config and canonical in config:
            legacy_value, canonical_value = (normalize_value(canonical, config[key]) for key in (legacy, canonical))
            if not same_value(legacy_value, canonical_value):
                conflicts.append(canonical)
            del config[legacy]
    return config, conflicts


def normalize_config(config, skip=()):
    """Return a shallow canonical copy; never mutate input or traverse extension JSON.

    Refuse future schema versions and conflicting aliases instead of overwriting content.
    The converter is idempotent, including mixed legacy/canonical records. Keys in
    ``skip`` (fields a project declares itself) are copied unchanged.
    """
    if not isinstance(config, dict):
        raise ValueError("Frontend configuration must be an object")
    version = config.get(VERSION_KEY, VERSION)
    if type(version) is not int or version != VERSION:
        raise ValueError("Unsupported universal token schema version")
    result = {}
    for key, value in config.items():
        if key in skip:
            result[key] = value
            continue
        name = canonical_key(key)
        normalized = normalize_value(name, value)
        if name in result and not same_value(result[name], normalized):
            raise ValueError(f"Conflicting legacy and canonical values for {name}")
        result[name] = normalized
    result[VERSION_KEY] = VERSION
    return result


FIELD_VALUES = {
    "container_type": ("bounded", "fluid", "full"),
    "vertical_alignment": ("start", "center", "end", "stretch", "baseline"),
    "horizontal_alignment": ("start", "center", "end", "between", "around", "evenly"),
    "column_alignment": ("start", "center", "end", "stretch", "baseline"),
    "card_type": ("group", "grid", "horizontal"),
    "inner_type": ("body", "header", "footer", "image-overlay"),
    "tab_type": ("tabs", "pills", "underline"),
    "tab_alignment": ("fill", "justified", "vertical", "start", "center", "end"),
    "link_type": ("link", "button"),
    "link_size": COMPONENT_SIZES,
    "carousel_transition": ("slide", "fade"),
    "background_shadow": SHADOWS,
    "alert_shadow": SHADOWS,
    "space_property": ("margin", "padding"),
    "space_sides": SIDES,
    "space_size": SPACING + ("auto",),
    "gutters": SPACING,
    "space_device": BREAKPOINTS,
    "navbar_breakpoint": BREAKPOINTS,
    "size_x": (
        "percent-25",
        "percent-50",
        "percent-75",
        "percent-100",
        "auto",
        "viewport",
        "dynamic-viewport",
        "min-content",
        "max-content",
    ),
    "size_y": (
        "percent-25",
        "percent-50",
        "percent-75",
        "percent-100",
        "auto",
        "viewport",
        "min-viewport",
        "dynamic-viewport",
        "min-content",
        "max-content",
    ),
    **{field: COLORS for field in COLOR_FIELDS},
    "background_context": COLORS + SURFACES,
    "card_text_color": FOREGROUNDS,
    "icon_foreground": FOREGROUNDS,
    "heading_context": FOREGROUNDS,
    "card_outline": COLORS + ("transparent",),
    "link_context": COLORS + ("link",),
}


def config_issues(config):
    """Describe values requiring project-specific decisions before a bulk conversion."""
    issues = []
    for field, value in config.items():
        if value is None or value == "":
            continue
        if field == "background_opacity" and (type(value) is not int or not 0 <= value <= 100):
            issues.append(f"{field}={value!r} is not a percentage")
        elif field in FIELD_VALUES and value not in FIELD_VALUES[field]:
            issues.append(f"{field}={value!r} has no universal mapping")
        elif field in DEVICE_LIST_FIELDS:
            if not isinstance(value, (list, tuple)) or any(bp not in BREAKPOINTS for bp in value):
                issues.append(f"{field}={value!r} contains unknown breakpoints")
        elif field in SPACING_FIELDS:
            if (
                not isinstance(value, dict)
                or set(value) != {"property", "side", "size"}
                or value.get("property") not in ("margin", "padding")
                or value.get("side") not in SIDES
                or value.get("size") not in SPACING + ("auto",)
                or value.get("property") == "padding"
                and value.get("size") == "auto"
            ):
                issues.append(f"{field}={value!r} has no universal spacing mapping")
    if config.get("space_property") == "padding" and config.get("space_size") == "auto":
        issues.append("Padding cannot use auto spacing")
    return issues
