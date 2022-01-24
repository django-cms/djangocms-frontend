class CardRenderMixin:
    def render(self, context, instance, placeholder):
        link_classes = [instance.card_type]
        if instance.card_context and instance.card_outline:
            link_classes.append("border-{}".format(instance.card_context))
        elif instance.card_context:
            link_classes.append("bg-{}".format(instance.card_context))
        if instance.card_alignment:
            link_classes.append(instance.card_alignment)
        if instance.card_text_color:
            link_classes.append("text-{}".format(instance.card_text_color))
        if getattr(instance, "card_full_height", False):
            link_classes.append("h-100")
        context["add_classes"] = link_classes
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
