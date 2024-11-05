import warnings

from django.utils.module_loading import autodiscover_modules


class Components:
    _registry: dict = {}
    _discovered: bool = False

    def register(self, component):
        if component.__name__ in self._registry:
            warnings.warn(f"Component {component.__name__} already registered", stacklevel=2)
            return component
        self._registry[component.__name__] = component.get_registration()
        return component

    def __getitem__(self, item):
        return self._registry[item]


components = Components()

if not components._discovered:
    autodiscover_modules("cms_components", register_to=components)
    components._discovered = True
