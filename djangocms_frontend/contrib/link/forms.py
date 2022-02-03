from importlib import import_module

from cms.forms.utils import get_page_choices
from cms.models import Page
from django import forms
from django.conf import settings as django_settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models.fields.related import ManyToOneRel
from django.utils.encoding import force_text
from django.utils.translation import gettext as _
from django_select2.forms import Select2Widget
from djangocms_icon.fields import IconField

# from djangocms_link.models import TARGET_CHOICES
# from djangocms_link.validators import IntranetURLValidator
from entangled.forms import EntangledModelForm
from filer.fields.image import AdminFileFormField, FilerFileField
from filer.models import File

from ... import settings
from ...fields import AttributesFormField, ColoredButtonGroup
from ...models import FrontendUIItem
from .constants import LINK_CHOICES, LINK_SIZE_CHOICES, TARGET_CHOICES


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
LINK_MODELS = getattr(django_settings, "DJANGOCMS_FRONTEND_LINK_MODELS", [])


class SmartLinkField(forms.ChoiceField):
    widget = Select2Widget

    def __init__(self, *args, **kwargs):
        kwargs["choices"] = SmartLinkField.get_link_choices
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_link_choices(lang=None):
        available_objects = []

        for item in LINK_MODELS:
            if item["class_path"] != "cms.models.Page":
                # CMS pages are collected using a cms function to preserve hierarchy
                model = item["type"]
                parts = item["class_path"].rsplit(".", 1)
                cls = getattr(import_module(parts[0]), parts[1])
                queryset = cls.objects

                if "manager_method" in item:
                    queryset = getattr(queryset, item["manager_method"])()

                if "filter" in item:
                    for (k, v) in item["filter"].items():
                        try:
                            # Attempt to execute any callables in the filter dict.
                            item["filter"][k] = v()
                        except TypeError:
                            # OK, it wasn't a callable, so, leave it be
                            pass
                    queryset = queryset.filter(**item["filter"])
                else:
                    if "manager_method" not in item:
                        queryset = queryset.all()

                if "order_by" in item:
                    queryset = queryset.order_by(item["order_by"])

                available_objects.append(
                    {
                        "model": model,
                        "objects": list(queryset),
                    }
                )

        # Now create our list of choices for the <select> field
        object_choices = []
        type_id = ContentType.objects.get_for_model(Page).id
        for value, descr in get_page_choices(lang):
            if isinstance(descr, list):
                hierarchy = []
                for page, name in descr:
                    hierarchy.append((f"{type_id}-{page}", name))
                object_choices.append((value, hierarchy))
            else:
                object_choices.append((value, descr))

        for group in available_objects:
            obj_list = []
            for obj in group["objects"]:
                type_class = ContentType.objects.get_for_model(obj.__class__)
                form_value = f"{type_class.id}-{obj.id}"
                display_text = str(obj)

                obj_list.append((form_value, display_text))
            object_choices.append(
                (
                    group["model"],
                    obj_list,
                )
            )
        return object_choices

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
        value = super().clean(value)
        if "-" in value:
            type_id, obj_id = value.split("-", 1)
            try:
                content_type = ContentType.objects.get(id=type_id)
                return dict(
                    model=f"{content_type.app_label}.{content_type.model}",
                    pk=int(obj_id),
                )
            except ObjectDoesNotExist:
                pass
        return None


class AbstractLinkForm(EntangledModelForm):
    class Meta:
        entangled_fields = {
            "config": [
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

    # url_validators = [
    #     IntranetURLValidator(intranet_host_re=HOSTNAME),
    # ]

    name = forms.CharField(
        label=_("Display name"),
        required=False,
    )
    external_link = forms.CharField(
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
                "template",
                "link_type",
                "link_context",
                "link_size",
                "link_outline",
                "link_block",
                "icon_left",
                "icon_right",
                "attributes",
            ]
        }
        untangled_fields = ()

    template = forms.ChoiceField(
        label=_("Template"),
        choices=get_templates(),
        initial=get_templates()[0][0],
    )
    link_type = forms.ChoiceField(
        label=_("Type"),
        choices=LINK_CHOICES,
        initial=LINK_CHOICES[0][0],
        widget=forms.RadioSelect(attrs={"class": "inline-block"}),
        help_text=_("Adds either the .btn-* or .text-* classes."),
    )
    link_context = forms.ChoiceField(
        label=_("Context"),
        choices=settings.EMPTY_CHOICE + settings.COLOR_STYLE_CHOICES,
        initial=settings.EMPTY_CHOICE[0][0],
        required=False,
        widget=ColoredButtonGroup(),
    )
    link_size = forms.ChoiceField(
        label=_("Size"),
        choices=LINK_SIZE_CHOICES,
        initial=LINK_SIZE_CHOICES[1][0],  # Medium
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
        initial="",
        required=False,
    )
    icon_right = IconField(
        label=_("Icon right"),
        initial="",
        required=False,
    )
    attributes = AttributesFormField()
