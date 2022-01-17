class ListGroupRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "list-group"
        if instance.list_group_flush:
            context["add_classes"] += " list-group-flush"
        return super().render(context, instance, placeholder)


class ListGroupItemRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "list-group-item"
        if instance.list_context:
            context["add_classes"] += " list-group-item-{}".format(
                instance.list_context
            )
        if instance.list_state:
            context["add_classes"] += " " + instance.list_state

        return super().render(context, instance, placeholder)
