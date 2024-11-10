from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm

from djangocms_frontend import settings
from djangocms_frontend.common import BackgroundFormMixin
from djangocms_frontend.contrib import navigation
from djangocms_frontend.contrib.link.forms import AbstractLinkForm, LinkForm
from djangocms_frontend.fields import AttributesFormField, ButtonGroup, IconGroup, TemplateChoiceMixin
from djangocms_frontend.helpers import first_choice
from djangocms_frontend.models import FrontendUIItem
from djangocms_frontend.settings import NAVBAR_DESIGNS

mixin_factory = settings.get_forms(navigation)


class NavigationForm(
    mixin_factory("Navigation"),
    BackgroundFormMixin,
    TemplateChoiceMixin,
    EntangledModelForm,
):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "template",
                "navbar_container",
                "navbar_design",
                "navbar_breakpoint",
                "attributes",
            ]
        }
        untangled_fields = ()

    template = forms.ChoiceField(
        label=_("Layout"),
        choices=settings.NAVIGATION_TEMPLATE_CHOICES,
        initial=first_choice(settings.NAVIGATION_TEMPLATE_CHOICES),
        help_text=_("Defines the whole template set for this navigation."),
    )
    navbar_container = forms.BooleanField(
        label=_("Container"),
        required=False,
        initial=True,
    )
    navbar_design = forms.ChoiceField(
        label=_("Design"),
        required=True,
        choices=NAVBAR_DESIGNS,
        initial=first_choice(NAVBAR_DESIGNS),
        widget=ButtonGroup(attrs=dict(property="nav-design")),
    )
    navbar_breakpoint = forms.ChoiceField(
        label=_("Expand on device (and larger)"),
        required=False,
        choices=settings.EMPTY_CHOICE + settings.DEVICE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        widget=IconGroup(),
    )
    attributes = AttributesFormField()


class PageTreeForm(mixin_factory("PageTree"), EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "start_level",
                "attributes",
            ]
        }
        untangled_fields = ()

    start_level = forms.IntegerField(
        label=_("Start level"),
        initial=0,
        help_text=_("Start level of this page tree (0: root, 1: level below root, etc.)"),
    )
    attributes = AttributesFormField()


class NavBrandForm(mixin_factory("NavBrand"), AbstractLinkForm, EntangledModelForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "simple_content",
                "attributes",
            ]
        }
        untangled_fields = ()

    link_is_optional = True

    simple_content = forms.CharField(
        label=_("Brand"),
        required=True,
        help_text=_("Enter brand name or add child plugins for brand icon or image"),
    )
    attributes = AttributesFormField()


class NavLinkForm(mixin_factory("NavLink"), LinkForm):
    link_is_optional = True
