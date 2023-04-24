class IconRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/icon.html"

    def render(self, context, instance, placeholder):
        classes = instance.config.get("icon", {}).get("iconClass", "")
        instance.add_classes(*classes.split())
        context["icon_text"] = instance.config.get("icon", {}).get("iconText", "")
        size = instance.config.get("icon_size", "")
        if size:
            if size[-1] == "%":
                instance.add_attribute("style", f"font-size:{size};")
            else:
                instance.add_classes(size)
        if instance.config.get("icon_foreground", None):
            instance.add_classes(f"text-{instance.icon_foreground}")
        if instance.config.get("icon_rounded", False):
            instance.add_classes("text-center", "rounded", "rounded-circle")
            instance.add_attribute(
                "style",
                "display:inline-block;line-height:1.49em;height:1.42em;width:1.42em;",
            )
        return super().render(context, instance, placeholder)
