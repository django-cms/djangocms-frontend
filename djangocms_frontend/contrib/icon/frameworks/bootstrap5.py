from django.templatetags.static import static

from djangocms_frontend.contrib.icon.conf import ICON_LIBRARIES


class IconRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/icon.html"

    def render(self, context, instance, placeholder):
        instance.tag_type = "span"
        classes = instance.config.get("icon", {}).get("iconClass", "")
        instance.add_classes(*classes.split())
        context["icon_text"] = instance.config.get("icon", {}).get("iconText", "")
        size = instance.config.get("icon_size", "")
        if size:
            if size[-1] == "%":
                instance.add_attribute("style", f"font-size:{size};")
            else:
                instance.add_classes(size)
        if instance.config.get("icon_foreground", None):
            instance.add_classes(f"text-{instance.icon_foreground}")
        if instance.config.get("icon_rounded", False):
            instance.add_classes("text-center", "rounded", "rounded-circle")
            instance.add_attribute(
                "style",
                "display:inline-block;line-height:1.42em;height:1.42em;width:1.42em;",
            )
        if instance.config.get("icon", {}).get("library", "") in ICON_LIBRARIES:
            css_link = ICON_LIBRARIES[instance.config.get("icon", {}).get("library")][1]
            if css_link:
                if "/" not in css_link:  # static link?
                    css_link = static(
                        f"djangocms_frontend/icon/vendor/assets/stylesheets/{css_link}"
                    )
                context["icon_css"] = css_link
        return super().render(context, instance, placeholder)
