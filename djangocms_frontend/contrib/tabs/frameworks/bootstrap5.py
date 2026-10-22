from djangocms_frontend.frameworks.bootstrap5_tokens import field_value


class TabRenderMixin:
    def render(self, context, instance, placeholder):
        if field_value(instance, "tab_alignment", "") == "flex-column":
            instance.add_classes("flex-row", "d-flex")
        return super().render(context, instance, placeholder)


class TabItemRenderMixin:
    def render(self, context, instance, placeholder):
        # Any parent: a project's own tab container need not subclass TabPlugin.
        parent = instance.get_parent_plugin_instance()
        if parent is None:
            instance.add_classes("tab-pane")
            return super().render(context, instance, placeholder)
        instance.add_classes("tab-pane", getattr(parent, "tab_effect", ""))
        tab_type = field_value(parent, "tab_type")
        if instance.config.get("tab_bordered", False):
            if tab_type == "nav-tabs":
                instance.add_classes("border-end border-start border-bottom")
            else:
                instance.add_classes("border")
        if tab_type == "nav-tabs":
            instance.add_classes("bg-body")
        if getattr(parent, "tab_index", None) == context.get("parentloop", {}).get("counter"):
            instance.add_classes("show active")
        return super().render(context, instance, placeholder)
