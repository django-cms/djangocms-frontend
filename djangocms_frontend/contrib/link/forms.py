from django import apps, forms
from django.conf import settings as django_settings
from django.contrib.sites.models import Site
from django.utils.translation import gettext as _
from djangocms_link.fields import LinkFormField

# from djangocms_link.validators import IntranetURLValidator
from entangled.forms import EntangledModelForm, EntangledModelFormMixin

from ... import settings
from ...common import SpacingFormMixin
from ...fields import AttributesFormField, ButtonGroup, ColoredButtonGroup, TagTypeFormField, TemplateChoiceMixin
from ...helpers import first_choice
from ...models import FrontendUIItem
from .. import link
from .constants import LINK_CHOICES, LINK_SIZE_CHOICES, TARGET_CHOICES

mixin_factory = settings.get_forms(link)

if "djangocms_frontend.contrib.icon" in django_settings.INSTALLED_APPS:
    # Weak dependency on djangocms_frontend.contrib.icon
    from djangocms_frontend.contrib.icon.fields import IconPickerField
elif "djangocms_icon" in django_settings.INSTALLED_APPS:  # pragma: no cover
    # Weak dependency on djangocms_icon
    # (Even if djangocms_icon is in the python path, the admin form will fail due to missing
    # templates if it's not in INSTALLED_APPS)
    from djangocms_icon.fields import IconField as IconPickerField
else:  # pragma: no cover

    class IconPickerField(forms.CharField):  # lgtm [py/missing-call-to-init]
        def __init__(self, *args, **kwargs):
            kwargs["widget"] = forms.HiddenInput
            super().__init__(*args, **kwargs)


if apps.apps.is_installed("djangocms_url_manager"):
    from djangocms_url_manager.forms import HtmlLinkSiteSelectWidget, HtmlLinkUrlSelectWidget
    from djangocms_url_manager.models import UrlGrouper

    class LinkFormMixin(EntangledModelFormMixin):
        class Meta:
            entangled_fields = {
                "config": [
                    "site",
                    "url_grouper",
                ]
            }

        site = forms.ModelChoiceField(
            label=_("Site"),
            queryset=Site.objects.all(),
            widget=HtmlLinkSiteSelectWidget(attrs={"data-placeholder": _("Select site")}),
            required=False,
        )
        url_grouper = forms.ModelChoiceField(
            label=_("Url"),
            queryset=UrlGrouper.objects.all(),
            widget=HtmlLinkUrlSelectWidget(attrs={"data-placeholder": _("Select URL object from list")}),
            required=False,
        )

else:

    class LinkFormMixin(EntangledModelFormMixin):
        class Meta:
            entangled_fields = {
                "config": [
                    "link",
                    "target",
                ]
            }

        link_is_optional = False

        link = LinkFormField(
            label=_("Link"),
            required=False,
        )
        target = forms.ChoiceField(
            label=_("Target"),
            choices=settings.EMPTY_CHOICE + TARGET_CHOICES,
            required=False,
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["link"].required = not self.link_is_optional


class AbstractLinkForm(LinkFormMixin, EntangledModelForm):
    pass


class LinkForm(mixin_factory("Link"), SpacingFormMixin, TemplateChoiceMixin, AbstractLinkForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "name",
                "template",
                "link_type",
                "link_context",
                "link_size",
                "link_outline",
                "link_block",
                "icon_left",
                "icon_right",
                "link_stretched",
                "attributes",
            ]
        }
        untangled_fields = ()
        exclude = ("ui_item",)

    name = forms.CharField(
        label=_("Display name"),
        required=False,
        widget=forms.TextInput(attrs={"class": "js-prepopulate-selected-text"}),
    )
    template = forms.ChoiceField(
        label=_("Layout"),
        choices=settings.LINK_TEMPLATE_CHOICES,
        initial=first_choice(settings.LINK_TEMPLATE_CHOICES),
    )
    link_stretched = forms.BooleanField(
        label=_("Stretch link"),
        required=False,
        initial=False,
        help_text=_("Stretches the active link area to the containing block (with position: relative)."),
    )
    link_type = forms.ChoiceField(
        label=_("Type"),
        choices=LINK_CHOICES,
        initial=first_choice(LINK_CHOICES),
        widget=forms.RadioSelect(attrs={"class": "inline-block"}),
        help_text=_("Adds either a text link or a button which links to the target."),
    )
    link_context = forms.ChoiceField(
        label=_("Context"),
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ColoredButtonGroup(),
    )
    link_size = forms.ChoiceField(
        label=_("Button size"),
        choices=LINK_SIZE_CHOICES,
        initial=LINK_SIZE_CHOICES[1][0],  # Medium
        required=False,
        widget=ButtonGroup(attrs=dict(property="link-size", label_class="btn-secondary")),
    )
    link_outline = forms.BooleanField(
        label=_("Outline"),
        initial=False,
        required=False,
        help_text=_("Removes the coloring from a button and keeps the outline."),
    )
    link_block = forms.BooleanField(
        label=_("Block"),
        initial=False,
        required=False,
        help_text=_("Extends the button to the width of its container."),
    )
    icon_left = IconPickerField(
        label=_("Icon left"),
        initial="",
        required=False,
    )
    icon_right = IconPickerField(
        label=_("Icon right"),
        initial="",
        required=False,
    )
    attributes = AttributesFormField()
    tag_type = TagTypeFormField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # name_required is set by the plugin's get_form method if needed
        self.fields["name"].required = getattr(self, "name_required", False)
