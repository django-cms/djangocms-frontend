class TabItemRenderMixin:
    def render(self, context, instance, placeholder):
        parent = instance.parent.get_plugin_instance()[0]
        instance.add_classes("tab-pane", parent.tab_effect)
        if (instance.config.get("tab_padding_size", "") or "0") != "0":
            instance.add_classes(
                f"p{instance.config.get('tab_padding_sides', '')}-{instance.config['tab_padding_size']}"
            )
        if instance.config.get("tab_bordered", False):
            instance.add_classes("border-end border-start border-bottom")
        if context["parent"].tab_type == "nav-tabs":
            instance.add_classes("bg-white")
        if parent.tab_index == context["parentloop"]["counter"]:
            instance.add_classes("show active")
        return super().render(context, instance, placeholder)
