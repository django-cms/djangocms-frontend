from __future__ import annotations

from cms.plugin_pool import plugin_pool

from .ui_plugin_base import CMSUIPluginBase


class CMSUIPlugin(CMSUIPluginBase):
    pass


def update_plugin_pool():
    from .component_pool import components

    # Loop through the values in the components' registry
    for _, plugin, slot_plugins in components._registry.values():
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
