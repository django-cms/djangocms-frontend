class ImageRenderMixin:
    def render(self, context, instance, placeholder):
        classes = "align-{}".format(instance.alignment) if instance.alignment else ""
        # assign link to a context variable to be performant
        context["picture_link"] = instance.get_link()
        context["picture_size"] = instance.get_size(
            width=context.get("width", 0),
            height=context.get("height", 0),
        )
        context["img_srcset_data"] = instance.img_srcset_data
        if instance.picture_fluid:
            classes += " img-fluid"
        if instance.picture_rounded:
            classes += " rounded"
        if instance.picture_thumbnail:
            classes += " img-thumbnail"
        if instance.parent and instance.parent.plugin_type == "CardPlugin":
            classes += " card-img-top" if instance.position == 0 else " card-img-bottom"
        context["add_classes"] = classes
        return super().render(context, instance, placeholder)
