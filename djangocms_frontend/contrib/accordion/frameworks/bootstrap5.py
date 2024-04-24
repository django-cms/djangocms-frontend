class AccordionRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/accordion.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("accordion")
        if instance.accordion_flush:
            instance.add_classes("accordion-flush")
        return super().render(context, instance, placeholder)


class AccordionItemRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/accordion_item.html"

    def render(self, context, instance, placeholder):
        instance.add_classes("accordion-collapse collapse")
        if instance.accordion_item_open:
            instance.add_classes("show")
        instance.font_size = context["parent"].config.get("accordion_header_type", "").replace("h", "fs-")
        return super().render(context, instance, placeholder)
