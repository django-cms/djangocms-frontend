from djangocms_frontend import settings

global_options = settings.FORM_OPTIONS


def get_option(form, option, default=None):
    form_options = getattr(getattr(form, "Meta", None), "options", {})
    return form_options.get(option, global_options.get(option, default))
