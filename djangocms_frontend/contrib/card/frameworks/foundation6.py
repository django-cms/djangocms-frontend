class CardRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("card")
        if instance.card_context and instance.card_outline:
            instance.add_classes(f"border-{instance.card_context}")
        elif instance.card_context:
            instance.add_classes(f"bg-{instance.card_context}")
        if instance.card_alignment:
            instance.add_classes(instance.card_alignment)
        if instance.card_text_color:
            instance.add_classes(f"text-{instance.card_text_color}")
        if getattr(instance, "card_full_height", False):
            instance.add_classes("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                instance.add_classes("h-100")
        return super().render(context, instance, placeholder)


class CardInnerRenderMixin:
    def render(self, context, instance, placeholder):
        if instance.inner_type == "card-body":
            instance.add_classes("card-section")
        elif instance.inner_type in ("card-header", "card-footer"):
            instance.add_classes("card-divider")
        # if instance.card_context and instance.card_outline:
        #     instance.add_classes(f"border-{instance.card_context}")
        # elif instance.card_context:
        #     instance.add_classes(f"bg-{instance.card_context}")
        if getattr(instance, "card_alignment", ""):
            instance.add_classes(instance.card_alignment)
        # if instance.card_text_color:
        #     instance.add_classes(f"text-{instance.card_text_color}")
        # if getattr(instance, "card_full_height", False):
        #     instance.add_classes("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                instance.add_classes("h-100")
        return super().render(context, instance, placeholder)
