"""Example components built on :class:`CMSFrontendComponent`.

``Tabs`` is a drop-in reimplementation of ``djangocms_frontend.contrib.tabs``
using the nested-component declaration: the repeating tab items are declared as
a nested ``Item`` class instead of a separately registered plugin. It reuses the
contrib tab templates and render mixins, so it renders byte-identically to the
built-in tabs plugin (see ``tests/test_component_examples.py``).

``Section`` demonstrates double nesting (``Section`` > ``Row`` > ``Col``) and the
``children`` template filter.
"""

from django import forms
from django.utils.translation import gettext_lazy as _

from djangocms_frontend import settings
from djangocms_frontend.common import AttributesMixin, PaddingMixin
from djangocms_frontend.component_base import CMSFrontendComponent
from djangocms_frontend.component_pool import components
from djangocms_frontend.contrib import tabs as tabs_module
from djangocms_frontend.contrib.tabs.constants import (
    TAB_ALIGNMENT_CHOICES,
    TAB_EFFECT_CHOICES,
    TAB_TEMPLATE_CHOICES,
    TAB_TYPE_CHOICES,
)
from djangocms_frontend.fields import AttributesFormField, ButtonGroup, IconGroup
from djangocms_frontend.helpers import first_choice

# Framework-specific render mixins, resolved exactly like the contrib plugin so
# the same CSS classes are added during rendering.
tab_renderer = settings.get_renderer(tabs_module)


@components.register
class Tabs(CMSFrontendComponent):
    # Same render mixins, in the same order, as contrib's TabPlugin.
    _plugin_mixins = [tab_renderer("Tab"), AttributesMixin]

    class Meta:
        name = _("Tabs (component)")
        module = _("Examples")
        # Own templates that render the tab items via the `children` filter;
        # get_render_template inserts the selected template folder ("default")
        # before the file name. Output is byte-identical to contrib.tabs.
        render_template = "examples/tabs/tabs.html"
        change_form_template = "djangocms_frontend/admin/tabs.html"

    template = forms.ChoiceField(
        label=_("Layout"),
        choices=TAB_TEMPLATE_CHOICES,
        initial=first_choice(TAB_TEMPLATE_CHOICES),
    )
    tab_type = forms.ChoiceField(
        label=_("Type"),
        choices=TAB_TYPE_CHOICES,
        initial=first_choice(TAB_TYPE_CHOICES),
        widget=ButtonGroup(attrs=dict(property="text")),
    )
    tab_alignment = forms.ChoiceField(
        label=_("Alignment"),
        choices=settings.EMPTY_CHOICE + TAB_ALIGNMENT_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=IconGroup(),
    )
    tab_index = forms.IntegerField(
        label=_("Index"),
        min_value=1,
        required=False,
        help_text=_("Index of element to open on page load starting at 1."),
    )
    tab_effect = forms.ChoiceField(
        label=_("Animation effect"),
        choices=settings.EMPTY_CHOICE + TAB_EFFECT_CHOICES,
        required=False,
    )
    attributes = AttributesFormField()

    def get_short_description(self):
        text = f"({self.config.get('tab_type', '')})"
        if self.config.get("tab_alignment"):
            text += f" .{self.config['tab_alignment']}"
        return text

    class Item(CMSFrontendComponent):
        # Same render mixins, in the same order, as contrib's TabItemPlugin.
        _plugin_mixins = [tab_renderer("TabItem"), AttributesMixin, PaddingMixin]

        class Meta:
            name = _("Tab item (component)")
            module = _("Examples")
            render_template = "examples/tabs/item.html"
            change_form_template = "djangocms_frontend/admin/tabs.html"

        tab_title = forms.CharField(label=_("Tab title"), initial=_("New tab"), required=True)
        tab_bordered = forms.BooleanField(
            label=_("Bordered"),
            required=False,
            help_text=_("Add borders to the tab item"),
        )
        attributes = AttributesFormField()

        def get_short_description(self):
            return self.config.get("tab_title", "")


@components.register
class Section(CMSFrontendComponent):
    """Double-nested layout component: Section > Row > Col."""

    class Meta:
        name = _("Section (component)")
        module = _("Examples")
        render_template = "examples/section/section.html"

    class Row(CMSFrontendComponent):
        class Meta:
            name = _("Row")
            module = _("Examples")
            render_template = "examples/section/row.html"

        class Col(CMSFrontendComponent):
            class Meta:
                name = _("Column")
                module = _("Examples")
                render_template = "examples/section/col.html"
                allow_children = True  # holds arbitrary content plugins
