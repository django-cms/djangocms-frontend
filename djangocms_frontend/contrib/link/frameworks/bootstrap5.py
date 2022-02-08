class LinkRenderMixin:
    def render(self, context, instance, placeholder):
        link_classes = []
        if instance.parent and instance.parent.plugin_type == "ListGroupPlugin":
            link_classes.append("list-group-item")
            link_classes.append("list-group-item-action")
            background_prefix = "list-group-item"
        elif (
            getattr(instance, "link_type", "link") == "link"
            and instance.parent
            and instance.parent.plugin_type == "CardInnerPlugin"
        ):
            link_classes.append("card-link")
        else:
            background_prefix = "btn"
        if instance.link_context:
            if getattr(instance, "link_type", "link") == "link":
                link_classes.append(f"link-{instance.link_context}")
            else:
                link_classes.append("btn")
                if not instance.link_outline:
                    link_classes.append(f"{background_prefix}-{instance.link_context}")
                else:
                    link_classes.append(f"btn-outline-{instance.link_context}")
        if instance.link_size:
            link_classes.append(instance.link_size)
        if instance.link_block:
            link_classes.append("btn-block")

        context["link"] = instance.get_link()
        instance.add_classes(link_classes)
        return super().render(context, instance, placeholder)
