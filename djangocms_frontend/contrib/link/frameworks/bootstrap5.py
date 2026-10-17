from djangocms_frontend.frameworks.bootstrap5_tokens import field_value
from djangocms_frontend.models import is_plugin_type


class LinkRenderMixin:
    def render(self, context, instance, placeholder):
        link_classes = []
        # A missing link_type is a link; any other value, even an empty or unknown
        # one, renders as a button (as before universal tokens).
        kind = field_value(instance, "link_type", "button") if "link_type" in instance.config else "link"
        color = field_value(instance, "link_context")
        if instance.parent and is_plugin_type(instance.parent.plugin_type, "ListGroupPlugin"):
            link_classes.append("list-group-item")
            link_classes.append("list-group-item-action")
            background_prefix = "list-group-item"
        elif kind == "link" and instance.parent and is_plugin_type(instance.parent.plugin_type, "CardInnerPlugin"):
            link_classes.append("card-link")
        else:
            background_prefix = "btn"
        if color:
            if kind == "link":
                link_classes.append(f"link-{color}")
            else:
                link_classes.append("btn")
                if not instance.config.get("link_outline"):
                    link_classes.append(f"{background_prefix}-{color}")
                else:
                    link_classes.append(f"btn-outline-{color}")
        size = field_value(instance, "link_size", "")
        if size:
            link_classes.append(size)
        if instance.config.get("link_block", False):
            link_classes.append("d-block")
        if instance.config.get("link_stretched", False):
            link_classes.append("stretched-link")
        instance.add_classes(link_classes)
        return super().render(context, instance, placeholder)
