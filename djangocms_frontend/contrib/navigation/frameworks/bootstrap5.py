class NavigationRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes(
            "navbar",
            f"navbar-{instance.config.get('navbar_design', '')}",
            f"navbar-expand-{instance.config.get('navbar_breakpoint', '')}",
        )
        if instance.config.get("navbar_design", "") == "dark":
            instance.add_classes("bg-dark")
        return super().render(context, instance, placeholder)


class PageTreeRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("navbar-nav")
        return super().render(context, instance, placeholder)


class NavBrandRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("navbar-brand")
        return super().render(context, instance, placeholder)


class NavLinkRenderMixin:
    def render(self, context, instance, placeholder):
        instance.add_classes("nav-link")
        if instance.child_plugin_instances:
            instance.add_classes("dropdown-toggle")
        return super().render(context, instance, placeholder)
