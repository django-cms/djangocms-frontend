class ModalRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/modal.html"


class ModalContainerRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/modal-container.html"

    def render(self, context, instance, placeholder):
        return super().render(context, instance, placeholder)


class ModalInnerRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/modal-inner.html"

    def render(self, context, instance, placeholder):
        instance.add_classes(instance.inner_type)
        return super().render(context, instance, placeholder)


class ModalTriggerRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/modal-trigger.html"
