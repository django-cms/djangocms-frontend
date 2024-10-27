from cms.plugin_pool import plugin_pool

# Import the components from the current directory's models module
from .registry import components

# Loop through the values in the components' registry
for _, plugin, slot_plugins in components._registry.values():
    # Add the plugin to the global namespace
    globals()[plugin.__name__] = plugin
    # Register the plugin with the plugin pool
    plugin_pool.register_plugin(plugin)

    # Loop through the slot plugins associated with the current plugin
    for slot_plugin in slot_plugins:
        # Add the slot plugin to the global namespace
        globals()[slot_plugin.__name__] = slot_plugin
        # Register the slot plugin with the plugin pool
        plugin_pool.register_plugin(slot_plugin)