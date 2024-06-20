import warnings

from djangocms_frontend.contrib.component.components import components

# Register all component models for Django
# Component models are unmanaged and do not create migrations

if "_registered" not in globals():
    _registered = True
    for model, *_ in components._registry.values():
        globals()[model.__name__] = model
else:  # pragma: no cover
    warnings.warn("Second model registration", stacklevel=2)
