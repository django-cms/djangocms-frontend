class IconRenderMixin:
    def render(self, context, instance, placeholder):
        instance.tag_type = "span"
        classes = instance.config.get("icon", {}).get("iconClass", "")
        instance.add_classes(*classes.split())
        return super().render(context, instance, placeholder)
