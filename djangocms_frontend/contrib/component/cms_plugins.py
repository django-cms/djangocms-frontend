from cms.plugin_pool import plugin_pool

from .models import components

for _, plugin in components._registry.values():
    globals()[plugin.__name__] = plugin
    plugin_pool.register_plugin(plugin)
