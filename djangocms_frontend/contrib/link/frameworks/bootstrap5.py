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
        if instance.config.get("link_context", None):
            if getattr(instance, "link_type", "link") == "link":
                link_classes.append(f"link-{instance.link_context}")
            else:
                link_classes.append("btn")
                if not instance.config.get("link_outline"):
                    link_classes.append(f"{background_prefix}-{instance.link_context}")
                else:
                    link_classes.append(f"btn-outline-{instance.link_context}")
        if instance.config.get("link_size", False):
            link_classes.append(instance.link_size)
        if instance.config.get("link_block", False):
            link_classes.append("d-block")
        if instance.config.get("link_stretched", False):
            link_classes.append("stretched-link")
        instance.add_classes(link_classes)
        return super().render(context, instance, placeholder)
