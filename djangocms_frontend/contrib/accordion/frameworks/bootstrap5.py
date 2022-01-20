class AccordionRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "accordion-flush" if instance.accordion_flush else ""
        return super().render(context, instance, placeholder)


class AccordionItemRenderMixin:
    def render(self, context, instance, placeholder):
        context["add_classes"] = "accordion-collapse collapse"
        if instance.accordion_item_open:
            context["add_classes"] += " show"
        context["font_size"] = (
            context["parent"]
            .config.get("accordion_header_type", "")
            .replace("h", "fs-")
        )
        return super().render(context, instance, placeholder)
