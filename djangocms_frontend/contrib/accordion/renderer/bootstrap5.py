class AccordionRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "accordion-flush" if instance.accordion_flush else ""
        return super().render(context, instance, placeholder)


class AccordionItemRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "accordion-collapse"
        if not instance.accordion_item_open:
            context["add_classes"] += " collapse"
        return super().render(context, instance, placeholder)
