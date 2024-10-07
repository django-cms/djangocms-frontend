from djangocms_frontend.helpers import is_first_child


class ImageRenderMixin:
    def render(self, context, instance, placeholder):
        if instance.alignment:
            # See https://getbootstrap.com/docs/5.2/content/images/#aligning-images
            if instance.alignment != "center":
                instance.add_classes(f"float-{instance.alignment}")
            else:
                instance.add_classes("mx-auto d-block")
        if instance.picture_fluid:
            instance.add_classes("img-fluid")
        if instance.picture_rounded:
            instance.add_classes("rounded")
        if instance.picture_thumbnail:
            instance.add_classes("img-thumbnail")
        if instance.parent and instance.parent.plugin_type == "CardPlugin":
            instance.add_classes("card-img-top" if is_first_child(instance, instance.parent) else "card-img-bottom")
        elif instance.parent and instance.parent.plugin_type == "FigurePlugin":
            instance.add_classes("figure-img")
        return super().render(context, instance, placeholder)
