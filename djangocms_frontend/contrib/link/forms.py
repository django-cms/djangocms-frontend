from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ManyToOneRel
from django.utils.encoding import force_text
from django.utils.translation import gettext as _
from djangocms_icon.fields import IconField
from djangocms_link.fields import PageSearchField
from djangocms_link.models import TARGET_CHOICES
from djangocms_link.validators import IntranetURLValidator
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminFileFormField, FilerFileField
from filer.models import File

from djangocms_frontend.settings import COLOR_STYLE_CHOICES

from ... import settings
from ...models import FrontendUIItem
from .constants import LINK_CHOICES, LINK_SIZE_CHOICES


def get_templates():
    choices = [
        ("default", _("Default")),
    ]
    choices += getattr(
        settings,
        "DJANGOCMS_LINK_TEMPLATES",
        [],
    )
    return choices


HOSTNAME = getattr(settings, "DJANGOCMS_LINK_INTRANET_HOSTNAME_PATTERN", None)


class AbstractLinkForm(EntangledModelForm):
    class Meta:
        entangled_fields = {
            "config": [
                "template",
                "name",
                "external_link",
                "internal_link",
                "file_link",
                "anchor",
                "mailto",
                "phone",
                "target",
            ]
        }
        untangled_fields = ("attributes",)

    link_is_optional = False

    url_validators = [
        IntranetURLValidator(intranet_host_re=HOSTNAME),
    ]

    template = forms.ChoiceField(
        label=_("Template"),
        choices=get_templates(),
        initial=get_templates()[0][0],
    )
    name = forms.CharField(
        label=_("Display name"),
        required=False,
    )
    external_link = forms.CharField(
        label=_("External link"),
        required=False,
        validators=url_validators,
        help_text=_("Provide a link to an external source."),
    )
    internal_link = PageSearchField(
        label=_("Internal link"),
        required=False,
        help_text=_("If provided, overrides the external link."),
    )
    file_link = AdminFileFormField(
        rel=ManyToOneRel(FilerFileField, File, "id"),
        queryset=File.objects.all(),
        to_field_name="id",
        label=_("File link"),
        required=False,
        help_text=_("If provided links a file from the filer app."),
    )
    # other link types
    anchor = forms.CharField(
        label=_("Anchor"),
        required=False,
        help_text=_(
            "Appends the value only after the internal or external link. "
            'Do <em>not</em> include a preceding "#" symbol.'
        ),
    )
    mailto = forms.EmailField(
        label=_("Email address"),
        required=False,
    )
    phone = forms.CharField(
        label=_("Phone"),
        required=False,
    )
    # advanced options
    target = forms.ChoiceField(
        label=_("Target"),
        choices=settings.EMPTY_CHOICE + TARGET_CHOICES,
        required=False,
    )

    def for_site(self, site):
        # override the internal_link fields queryset to contains just pages for
        # current site
        # this will work for PageSelectFormField
        from cms.models import Page

        self.fields["internal_link"].queryset = Page.objects.drafts().on_site(site)
        # set the current site as a internal_link field instance attribute
        # this will be used by the field later to properly set up the queryset
        # this will work for PageSearchField
        self.fields["internal_link"].site = site
        self.fields["internal_link"].widget.site = site

    def clean(self):
        super().clean()
        link_field_names = (
            "external_link",
            "internal_link",
            "mailto",
            "phone",
            "file_link",
        )
        anchor_field_name = "anchor"
        field_names_allowed_with_anchor = (
            "external_link",
            "internal_link",
        )
        anchor_field_verbose_name = force_text(self.fields[anchor_field_name].label)
        anchor_field_value = self.cleaned_data[anchor_field_name]

        link_fields = {key: self.cleaned_data[key] for key in link_field_names}
        link_field_verbose_names = {
            key: force_text(self.fields[key].label) for key in link_fields.keys()
        }
        provided_link_fields = {
            key: value for key, value in link_fields.items() if value
        }

        if len(provided_link_fields) > 1:
            # Too many fields have a value.
            verbose_names = sorted(link_field_verbose_names.values())
            error_msg = _("Only one of {0} or {1} may be given.").format(
                ", ".join(verbose_names[:-1]),
                verbose_names[-1],
            )
            errors = {}.fromkeys(provided_link_fields.keys(), error_msg)
            raise ValidationError(errors)

        if (
            len(provided_link_fields) == 0
            and not self.cleaned_data[anchor_field_name]
            and not self.link_is_optional
        ):
            raise ValidationError(_("Please provide a link."))

        if anchor_field_value:
            for field_name in provided_link_fields.keys():
                if field_name not in field_names_allowed_with_anchor:
                    error_msg = _(
                        "%(anchor_field_verbose_name)s is not allowed together with %(field_name)s"
                    ) % {
                        "anchor_field_verbose_name": anchor_field_verbose_name,
                        "field_name": link_field_verbose_names.get(field_name),
                    }
                    raise ValidationError(
                        {
                            anchor_field_name: error_msg,
                            field_name: error_msg,
                        }
                    )


class LinkForm(AbstractLinkForm):
    class Meta:
        model = FrontendUIItem
        entangled_fields = {
            "config": [
                "link_type",
                "link_context",
                "link_size",
                "link_outline",
                "link_block",
                "icon_left",
                "icon_right",
            ]
        }

    link_type = forms.ChoiceField(
        label=_("Type"),
        choices=LINK_CHOICES,
        initial=LINK_CHOICES[0][0],
        widget=forms.RadioSelect(attrs={"class": "inline-block"}),
        help_text=_("Adds either the .btn-* or .text-* classes."),
    )
    link_context = forms.ChoiceField(
        label=_("Context"), choices=COLOR_STYLE_CHOICES, required=False
    )
    link_size = forms.ChoiceField(
        label=_("Size"),
        choices=LINK_SIZE_CHOICES,
        required=False,
    )
    link_outline = forms.BooleanField(
        label=_("Outline"),
        initial=False,
        required=False,
        help_text=_("Applies the .btn-outline class to the elements."),
    )
    link_block = forms.BooleanField(
        label=_("Block"),
        initial=False,
        required=False,
        help_text=_("Extends the button to the width of its container."),
    )
    icon_left = IconField(
        label=_("Icon left"),
        required=False,
    )
    icon_right = IconField(
        label=_("Icon right"),
        required=False,
    )

    # def get_form(self, request, obj=None, **kwargs):
    #     form_class = super().get_form(request, obj, **kwargs)
    #
    #     if obj and obj.page and hasattr(obj.page, 'site') and obj.page.site:
    #         site = obj.page.site
    #     elif self.page and hasattr(self.page, 'site') and self.page.site:
    #         site = self.page.site
    #     else:
    #         site = Site.objects.get_current()
    #
    #     class Form(form_class):
    #         def __init__(self, *args, **kwargs):
    #             super().__init__(*args, **kwargs)
    #             self.for_site(site)
    #
    #     return Form
