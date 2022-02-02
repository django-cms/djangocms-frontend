class CardRenderMixin:
    def render(self, context, instance, placeholder):
        card_classes = []
        if instance.card_context and instance.card_outline:
            card_classes.append("border-{}".format(instance.card_context))
        elif instance.card_context:
            card_classes.append("bg-{}".format(instance.card_context))
        if instance.card_alignment:
            card_classes.append(instance.card_alignment)
        if instance.card_text_color:
            card_classes.append("text-{}".format(instance.card_text_color))
        if getattr(instance, "card_full_height", False):
            card_classes.append("h-100")
        if instance.parent and instance.parent.plugin_type == "CardLayoutPlugin":
            if instance.parent.get_plugin_instance()[0].card_type == "row":
                card_classes.append("h-100")
        context["add_classes"] = card_classes
        return super().render(context, instance, placeholder)


class CardInnerRenderMixin:
    def render(self, context, instance, placeholder):
        context["inner_context"] = (
            f"bg-{instance.inner_context}"
            if getattr(instance, "inner_context", None)
            else ""
        )
        context["text_alignment"] = (
            f"text-{instance.text_alignment}"
            if getattr(instance, "text_alignment", None)
            else ""
        )
        return super().render(context, instance, placeholder)
