from cms.plugin_pool import plugin_pool
from django.core.exceptions import ImproperlyConfigured

from .ui_plugin_base import CMSUIPluginBase


class CMSUIPlugin(CMSUIPluginBase):
    pass


def update_plugin_pool():
    from .component_pool import components

    # Loop through the values in the components' registry
    for key, (_, plugin, slot_plugins) in components._registry.items():
        if plugin.__name__ not in plugin_pool.plugins:
            # Add the plugin to the global namespace
            globals()[plugin.__name__] = plugin
            # Register the plugin with the plugin pool
            plugin_pool.register_plugin(plugin)

            # Loop through the slot plugins associated with the current plugin
            for slot_plugin in slot_plugins:
                # Add the slot plugin to the global namespace
            # Register slot plugins, checking for name conflicts
            for slot_plugin in slot_plugins:
                if slot_plugin.__name__ not in plugin_pool.plugins:
                    globals()[slot_plugin.__name__] = slot_plugin
                    plugin_pool.register_plugin(slot_plugin)
                else:
                    raise ImproperlyConfigured(
                        f"Cannot register slot plugin {slot_plugin.__name__} "
                        f"since a plugin {slot_plugin.__name__} is already registered "
                        f"by {plugin_pool.plugins[slot_plugin.__name__].__module__}."
                    )
        else:
            raise ImproperlyConfigured(
                f"Cannot register frontend component {key} since a plugin {plugin.__name__} "
                f"is already registered by {plugin_pool.plugins[plugin.__name__].__module__}."
            )
