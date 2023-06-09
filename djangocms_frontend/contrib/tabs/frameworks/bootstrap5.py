class TabRenderMixin:
    def render(self, context, instance, placeholder):
        if instance.config.get("tab_alignment", "") == "flex-column":
            instance.add_classes("flex-row", "d-flex")
        return super().render(context, instance, placeholder)


class TabItemRenderMixin:
    def render(self, context, instance, placeholder):
        parent = instance.parent.get_plugin_instance()[0]
        instance.add_classes("tab-pane", parent.tab_effect)
        if instance.config.get("tab_bordered", False):
            if context["parent"].tab_type == "nav-tabs":
                instance.add_classes("border-end border-start border-bottom")
            else:
                instance.add_classes("border")
        if context["parent"].tab_type == "nav-tabs":
            instance.add_classes("bg-body")
        if parent.tab_index == context["parentloop"]["counter"]:
            instance.add_classes("show active")
        return super().render(context, instance, placeholder)
