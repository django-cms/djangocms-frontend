class TabItemRenderMixin:
    def render(self, context, instance, placeholder):
        if (instance.config.get("tab_padding_size", "") or "0") != "0":
            instance.add_classes = f"p{instance.config.get('tab_padding_sides', '')}-{instance.config['tab_padding_size']}"
        else:
            instance.add_classes = ""
        instance.add_classes += (
            " border-end border-start border-bottom"
            if instance.config.get("tab_bordered", False)
            else ""
        )
        if context["parent"].tab_type == "nav-tabs":
            instance.add_classes += " bg-white"
        return super().render(context, instance, placeholder)
