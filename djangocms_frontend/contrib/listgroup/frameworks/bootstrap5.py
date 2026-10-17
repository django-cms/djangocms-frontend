from djangocms_frontend.frameworks.bootstrap5_tokens import field_value


class ListGroupRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("list-group")
        if instance.list_group_flush:
            instance.add_classes("list-group-flush")
        return super().render(context, instance, placeholder)


class ListGroupItemRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("list-group-item")
        color = field_value(instance, "list_context")
        if color:
            instance.add_classes(f"list-group-item-{color}")
        if instance.list_state:
            instance.add_classes(instance.list_state)

        return super().render(context, instance, placeholder)
