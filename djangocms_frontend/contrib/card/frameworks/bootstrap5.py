from djangocms_frontend.contrib.grid.frameworks.bootstrap5 import (
    get_row_cols_grid_values,
)


class CardRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("card")
        if instance.card_context and instance.card_outline:
            instance.add_classes("border-{}".format(instance.card_context))
        elif instance.card_context:
            instance.add_classes("bg-{}".format(instance.card_context))
        if instance.card_alignment:
            instance.add_classes(instance.card_alignment)
        if instance.card_text_color:
            instance.add_classes("text-{}".format(instance.card_text_color))
        if getattr(instance, "card_full_height", False):
            instance.add_classes("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                instance.add_classes("h-100")
        return super().render(context, instance, placeholder)


class CardInnerRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.inner_type)
        if getattr(instance, "inner_context", None):
            instance.add_classes(f"bg-{instance.inner_context}")
        if getattr(instance, "text_alignment", None):
            instance.add_classes(f"text-{instance.text_alignment}")
        return super().render(context, instance, placeholder)


class CardLayoutRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(instance.card_type)
        instance.add_classes(get_row_cols_grid_values(instance))
        return super().render(context, instance, placeholder)
