import hashlib

from django.core.exceptions import ImproperlyConfigured
from django.core.mail import mail_admins, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from .entry_model import FormEntry
from .helper import get_option

_action_registry = {}


def get_registered_actions():
    """Creates a tuple for a ChoiceField to select form"""
    result = tuple(
        (hash, action_class.verbose_name)
        for hash, action_class in _action_registry.items()
    )
    return result if result else ((_("No actions registered"), ()),)


def register(action_class):
    """Function to call or decorator for an Action class to make it available for the
    djangocms_frontend.contrib.frontend_forms plugin"""

    if not issubclass(action_class, FormAction):
        raise ImproperlyConfigured(
            "djangocms_frontend.contrib.frontend_forms.actions.register only "
            "accets subclasses of djangocms_frontend.contrib.frontend_forms.actions.FormAction"
        )
    if not action_class.verbose_name:
        raise ImproperlyConfigured(
            "FormActions need to have a verbose_name property to be " "resitered"
        )
    hash = hashlib.sha1(action_class.__name__.encode("utf-8")).hexdigest()
    _action_registry.update({hash: action_class})
    return action_class


def get_action_class(action):
    return _action_registry.get(action, None)


class FormAction:
    verbose_name = None

    def execute(self, form, request):
        raise NotImplementedError()


@register
class SaveToDBAction(FormAction):
    verbose_name = _("Save form submission")

    def execute(self, form, request):
        if get_option(form, "unique", False) and get_option(
            form, "login_required", False
        ):
            keys = {
                "form_name": get_option(form, "form_name"),
                "form_user": request.user,
            }
            defaults = {}
        else:
            keys = {}
            defaults = {
                "form_name": get_option(form, "form_name"),
                "form_user": request.user,
            }
        defaults.update(
            {
                "entry_data": form.cleaned_data,
                "html_headers": dict(
                    user_agent=request.headers["User-Agent"],
                    referer=request.headers["Referer"],
                ),
            }
        )
        if keys:  # update_or_create only works if at least one key is given
            try:
                FormEntry.objects.update_or_create(**keys, defaults=defaults)
            except FormEntry.MultipleObjectsReturned:  # Delete outdated objects
                FormEntry.objects.filter(**keys).delete()
                FormEntry.objects.create(**keys, **defaults)
        else:
            FormEntry.objects.create(**defaults), True


SAVE_TO_DB_ACTION = next(iter(_action_registry)) if _action_registry else None


@register
class SendMailAction(FormAction):
    verbose_name = _("Send email to administrators")
    recipients = None
    from_mail = None
    template = "djangocms_frontend/actions/mail.html"
    subject = _("%(form_name)s form submission")

    def execute(self, form, request):
        context = dict(
            cleaned_data=form.cleaned_data,
            user=request.user,
            user_agent=request.headers["User-Agent"],
            referer=request.headers["Referer"],
        )
        html_message = render_to_string(self.template, context)
        message = strip_tags(html_message)
        if self.recipients is None:
            mail_admins(
                self.subject % dict(form_name=""),
                message,
                fail_silently=True,
                html_message=html_message,
            )
        else:
            send_mail(
                self.subject % dict(form_name=""),
                message,
                self.recipients,
                self.from_mail,
                fail_silently=True,
                html_message=html_message,
            )
