class ListGroupRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("list-group")
        if instance.list_group_flush:
            instance.add_classes("list-group-flush")
        return super().render(context, instance, placeholder)


class ListGroupItemRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("list-group-item")
        if instance.list_context:
            instance.add_classes(f"list-group-item-{instance.list_context}")
        if instance.list_state:
            instance.add_classes(instance.list_state)

        return super().render(context, instance, placeholder)
