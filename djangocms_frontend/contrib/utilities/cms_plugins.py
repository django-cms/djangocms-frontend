from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings

from ...cms_plugins import CMSUIPlugin
from ...common import AttributesMixin, SpacingMixin
from .. import utilities
from . import forms, models

mixin_factory = settings.get_renderer(utilities)


@plugin_pool.register_plugin
class SpacingPlugin(mixin_factory("Spacing"), AttributesMixin, CMSUIPlugin):
    """
    Components > "Card" Plugin
    https://getbootstrap.com/docs/5.0/components/card/
    """

    name = _("Spacing")
    module = _("Frontend")
    model = models.Spacing
    form = forms.SpacingForm

    change_form_template = "djangocms_frontend/admin/spacing.html"
    allow_children = True

    fieldsets = [
        (
            None,
            {
                "fields": (
                    "space_property",
                    "space_sides",
                    "space_size",
                    "space_device",
                )
            },
        ),
    ]


@plugin_pool.register_plugin
class EditorNotePlugin(mixin_factory("EditorNote"), CMSUIPlugin):
    """Room for notes for editor only visible in edit mode"""

    name = _("Editor note")
    module = _("Frontend")
    allow_children = True
    change_form_template = "djangocms_frontend/admin/no_form.html"
    show_add_form = False
    edit_disabled = True


@plugin_pool.register_plugin
class HeadingPlugin(mixin_factory("Heading"), AttributesMixin, SpacingMixin, CMSUIPlugin):
    """Room for notes for editor only visible in edit mode"""

    name = _("Heading")
    module = _("Frontend")
    model = models.Heading
    form = forms.HeadingForm

    render_template = "djangocms_frontend/heading.html"
    allow_children = True
    is_local = False

    fieldsets = [
        (
            None,
            {
                "fields": (
                    ("heading_level", "heading_id"),
                    "heading",
                    "heading_alignment",
                    "heading_context",
                )
            },
        ),
    ]

    frontend_editable_fields = ("heading",)

    def render(self, context, instance, placeholder):
        if not hasattr(context["request"], "TOC"):
            context["request"].TOC = []
        heading_id = getattr(instance, "heading_id", "")
        if heading_id:
            context["request"].TOC.append(
                (
                    heading_id,
                    getattr(instance, "heading", ""),
                    getattr(instance, "heading_level", "h2"),
                )
            )
        context["instance"] = instance
        return super().render(context, instance, placeholder)


def create_tree(request_toc):
    def process_level():
        nonlocal i

        previous_level = None
        toc_tree = []
        while i < len(request_toc):
            if previous_level is None or previous_level == request_toc[i][2]:
                toc_tree.append((request_toc[i][0], request_toc[i][1]))
                previous_level = request_toc[i][2]
                i += 1
            elif previous_level < request_toc[i][2]:
                toc_tree.append((None, process_level()))
            elif previous_level > request_toc[i][2]:
                break
        return toc_tree

    i = 0
    return process_level()


@plugin_pool.register_plugin
class TOCPlugin(mixin_factory("TOC"), AttributesMixin, CMSUIPlugin):
    name = _("Table of contents")
    module = _("Frontend")

    model = models.TableOfContents
    form = forms.TableOfContentsForm

    render_template = "djangocms_frontend/toc.html"
    change_form_template = "djangocms_frontend/admin/no_form.html"

    fieldsets = settings.EMPTY_FIELDSET
    show_add_form = False
    edit_disabled = True
    is_local = False

    def render(self, context, instance, placeholder):
        if hasattr(context["request"], "TOC"):
            toc_tree = create_tree(context["request"].TOC)
            context["toc"] = toc_tree
        else:
            context["toc"] = []
        context["template"] = self.render_template
        context["instance"] = instance
        return super().render(context, instance, placeholder)
