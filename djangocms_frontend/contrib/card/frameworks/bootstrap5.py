from djangocms_frontend.contrib.grid.frameworks.bootstrap5 import get_row_cols_grid_values
from djangocms_frontend.frameworks.bootstrap5_tokens import field_value


class CardRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/card.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("card")
        outline = field_value(instance, "card_outline")
        if outline:
            instance.add_classes(f"border-{outline}")
        if instance.card_alignment:
            instance.add_classes(f"text-{instance.card_alignment}")
        text_color = field_value(instance, "card_text_color")
        if text_color:
            instance.add_classes(f"text-{text_color}")
        if instance.config.get("card_full_height", None):
            instance.add_classes("h-100")
        if instance.get_parent_framework_value("CardLayoutPlugin", "card_type") == "row":
            instance.add_classes("h-100")
        return super().render(context, instance, placeholder)


class CardInnerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(field_value(instance, "inner_type"))
        if getattr(instance, "text_alignment", None):
            instance.add_classes(f"text-{instance.text_alignment}")
        return super().render(context, instance, placeholder)


class CardLayoutRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(field_value(instance, "card_type"))
        instance.add_classes(get_row_cols_grid_values(instance))
        return super().render(context, instance, placeholder)
