from djangocms_frontend.contrib.carousel.constants import CAROUSEL_DEFAULT_SIZE


class CarouselRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("carousel slide")
        return super().render(context, instance, placeholder)


class CarouselSlideRenderMixin:
    def render(self, context, instance, placeholder):
        parent = instance.parent.get_plugin_instance()[0]
        width = float(context.get("width") or CAROUSEL_DEFAULT_SIZE[0])
        height = float(context.get("height") or CAROUSEL_DEFAULT_SIZE[1])

        if parent.carousel_aspect_ratio:
            aspect_width, aspect_height = tuple(
                [int(i) for i in parent.carousel_aspect_ratio.split("x")]
            )
            height = width * aspect_height / aspect_width

        instance.add_classes("carousel-item")
        if instance.position == 0:
            instance.add_classes("active")
        context["link"] = instance.get_link()
        context["aspect_ratio"] = str(width / height)
        context["options"] = {"crop": 10, "size": (width, height), "upscale": True}
        return super().render(context, instance, placeholder)
