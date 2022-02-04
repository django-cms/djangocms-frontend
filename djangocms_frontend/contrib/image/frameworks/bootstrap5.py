class ImageRenderMixin:
    def render(self, context, instance, placeholder):
        # assign link to a context variable to be performant
        context["picture_link"] = instance.get_link()
        context["picture_size"] = instance.get_size(
            width=context.get("width", 0),
            height=context.get("height", 0),
        )
        context["img_srcset_data"] = instance.img_srcset_data
        if instance.alignment:
            instance.add_classes("align-{}".format(instance.alignment))
        if instance.picture_fluid:
            instance.add_classes("img-fluid")
        if instance.picture_rounded:
            instance.add_classes("rounded")
        if instance.picture_thumbnail:
            instance.add_classes("img-thumbnail")
        if instance.parent and instance.parent.plugin_type == "CardPlugin":
            instance.add_classes(
                "card-img-top" if instance.position == 0 else "card-img-bottom"
            )
        return super().render(context, instance, placeholder)
