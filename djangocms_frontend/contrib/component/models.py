from djangocms_frontend.contrib.component.components import components

# Register all component models for Django
# Component models are unmanaged and do not create migrations

for model, *_ in components._registry.values():
    globals()[model.__name__] = model
