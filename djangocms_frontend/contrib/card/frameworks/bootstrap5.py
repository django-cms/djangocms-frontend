from djangocms_frontend.contrib.grid.frameworks.bootstrap5 import get_row_cols_grid_values


class CardRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/card.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("card")
        if instance.config.get("card_outline", None):
            instance.add_classes(f"border-{instance.card_outline}")
        if instance.card_alignment:
            instance.add_classes(f"text-{instance.card_alignment}")
        if instance.config.get("card_text_color", None):
            instance.add_classes(f"text-{instance.card_text_color}")
        if instance.config.get("card_full_height", None):
            instance.add_classes("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                instance.add_classes("h-100")
        return super().render(context, instance, placeholder)


class CardInnerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.inner_type)
        if getattr(instance, "text_alignment", None):
            instance.add_classes(f"text-{instance.text_alignment}")
        return super().render(context, instance, placeholder)


class CardLayoutRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.card_type)
        instance.add_classes(get_row_cols_grid_values(instance))
        return super().render(context, instance, placeholder)
