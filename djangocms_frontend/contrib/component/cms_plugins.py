from cms.plugin_pool import plugin_pool

from .models import components

for _, plugin, slot_plugins in components._registry.values():
    globals()[plugin.__name__] = plugin
    plugin_pool.register_plugin(plugin)
    for slot_plugin in slot_plugins:
        globals()[slot_plugin.__name__] = slot_plugin
        plugin_pool.register_plugin(slot_plugin)
