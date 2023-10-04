from django import apps, forms
from django.conf import settings as django_settings
from django.contrib.admin.widgets import SELECT2_TRANSLATIONS
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models.fields.related import ManyToOneRel
from django.utils.encoding import force_str
from django.utils.translation import get_language
from django.utils.translation import gettext as _
from django_select2.forms import HeavySelect2Widget, Select2Widget

# from djangocms_link.validators import IntranetURLValidator
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminFileFormField, FilerFileField
from filer.models import File

from ... import settings
from ...common.spacing import SpacingFormMixin
from ...fields import (
    AttributesFormField,
    ButtonGroup,
    ColoredButtonGroup,
    TagTypeFormField,
    TemplateChoiceMixin,
)
from ...helpers import first_choice, get_related_object
from ...models import FrontendUIItem
from .. import link
from .constants import LINK_CHOICES, LINK_SIZE_CHOICES, TARGET_CHOICES
from .helpers import ensure_select2_url_is_available, get_choices, get_object_for_value

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


HOSTNAME = getattr(settings, "DJANGOCMS_LINK_INTRANET_HOSTNAME_PATTERN", None)
LINK_MODELS = getattr(django_settings, "DJANGOCMS_FRONTEND_LINK_MODELS", [])
MINIMUM_INPUT_LENGTH = getattr(
    django_settings, "DJANGOCMS_FRONTEND_MINIMUM_INPUT_LENGTH", 0
)


class Select2jqWidget(HeavySelect2Widget if MINIMUM_INPUT_LENGTH else Select2Widget):
    """Make jQuery available to Select2 widget"""

    empty_label = _("Select a destination")

    @property
    def media(self):
        extra = ".min"
        i18n_name = SELECT2_TRANSLATIONS.get(get_language())
        i18n_file = (
            ("admin/js/vendor/select2/i18n/%s.js" % i18n_name,) if i18n_name else ()
        )
        return forms.Media(
            js=("admin/js/vendor/select2/select2.full%s.js" % extra,)
            + i18n_file
            + ("djangocms_frontend/js/django_select2.js",),
            css={
                "screen": (
                    "admin/css/vendor/select2/select2%s.css" % extra,
                    "djangocms_frontend/css/select2.css",
                ),
            },
        )

    def __init__(self, *args, **kwargs):
        if MINIMUM_INPUT_LENGTH:
            if "attrs" in kwargs:
                kwargs["attrs"].setdefault(
                    "data-minimum-input-length", MINIMUM_INPUT_LENGTH
                )
            else:
                kwargs["attrs"] = {"data-minimum-input-length": MINIMUM_INPUT_LENGTH}
            kwargs.setdefault("data_view", "dcf_autocomplete:ac_view")
        super().__init__(*args, **kwargs)


class SmartLinkField(forms.ChoiceField):
    widget = Select2jqWidget

    def prepare_value(self, value):
        if value:
            if isinstance(value, dict):  # Entangled dictionary?
                try:
                    app_label, model = value["model"].rsplit(".", 1)
                    content_type = ContentType.objects.get(
                        app_label=app_label, model=model
                    )
                    return f"{content_type.id}-{value['pk']}"
                except (TypeError, ValueError, KeyError, ObjectDoesNotExist):
                    pass
            elif isinstance(value, models.Model):
                content_type = ContentType.objects.get_for_model(value)
                return f"{content_type.id}-{value.id}"
        return ""

    def clean(self, value):
        obj = get_object_for_value(value)
        if obj is not None:
            return obj
        return super().clean(value)


if apps.apps.is_installed("djangocms_url_manager"):
    from djangocms_url_manager.forms import (
        HtmlLinkSiteSelectWidget,
        HtmlLinkUrlSelectWidget,
    )
    from djangocms_url_manager.models import UrlGrouper

    class AbstractLinkForm(EntangledModelForm):
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
            widget=HtmlLinkSiteSelectWidget(
                attrs={"data-placeholder": _("Select site")}
            ),
            required=False,
        )
        url_grouper = forms.ModelChoiceField(
            label=_("Url"),
            queryset=UrlGrouper.objects.all(),
            widget=HtmlLinkUrlSelectWidget(
                attrs={"data-placeholder": _("Select URL object from list")}
            ),
            required=False,
        )

else:

    class AbstractLinkForm(EntangledModelForm):
        class Meta:
            entangled_fields = {
                "config": [
                    "external_link",
                    "internal_link",
                    "file_link",
                    "anchor",
                    "mailto",
                    "phone",
                    "target",
                ]
            }

        link_is_optional = False

        # url_validators = [
        #     IntranetURLValidator(intranet_host_re=HOSTNAME),
        # ]

        external_link = forms.URLField(
            label=_("External link"),
            required=False,
            #        validators=url_validators,
            help_text=_("Provide a link to an external source."),
        )
        internal_link = SmartLinkField(
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
                'Do <em>not</em> include a preceding "&#35;" symbol.'
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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            ensure_select2_url_is_available()
            self.fields["internal_link"].choices = self.get_choices

        def get_choices(self):
            if MINIMUM_INPUT_LENGTH == 0:
                return get_choices(self.request)
            if not self.is_bound:  # find inital value
                int_link_field = self.fields["internal_link"]
                initial = self.get_initial_for_field(int_link_field, "internal_link")
                if initial:  # Initial set?
                    obj = get_related_object(dict(obj=initial), "obj")  # get it!
                    if obj is not None:
                        value = int_link_field.prepare_value(initial)
                        return ((value, str(obj)),)
            return ()  # nothing found

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
            anchor_field_verbose_name = force_str(self.fields[anchor_field_name].label)
            anchor_field_value = self.cleaned_data.get(anchor_field_name, None)
            link_fields = {
                key: self.cleaned_data.get(key, None) for key in link_field_names
            }
            link_field_verbose_names = {
                key: force_str(self.fields[key].label) for key in link_fields.keys()
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
                and not self.cleaned_data.get(anchor_field_name, None)
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


class LinkForm(
    mixin_factory("Link"), SpacingFormMixin, TemplateChoiceMixin, AbstractLinkForm
):
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

    name = forms.CharField(
        label=_("Display name"),
        required=False,
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
        help_text=_(
            "Stretches the active link area to the containing block (with position: relative)."
        ),
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
        widget=ButtonGroup(
            attrs=dict(property="link-size", label_class="btn-secondary")
        ),
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
