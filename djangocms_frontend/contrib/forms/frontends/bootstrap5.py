default_attr = dict(
    input="form-control",
    label="form-label",
    div="",
    group="",
)

attr_dict = dict(
    Select=dict(input="form-select"),
    SelectMultiple=dict(input="form-select"),
    NullBooleanSelect=dict(input="form-select"),
    RadioSelect=dict(
        input="form-check-input", label="form-check-label", group="form-check"
    ),
    CheckboxInput=dict(
        input="form-check-input", label="form-check-label", div="form-check"
    ),
    SwitchInput=dict(
        input="form-check-input", label="form-check-label", div="form-check form-switch"
    ),
    CheckboxSelectMultiple=dict(
        input="form-check-input", label="form-check-label", group="form-check"
    ),
    ButtonRadio=dict(input="btn-check", label="btn btn-outline-primary"),
    ButtonCheckbox=dict(input="btn-check", label="btn btn-outline-primary"),
)

DEFAULT_FIELD_SEP = "mb-3"


class FormRenderMixin:
    render_template = "djangocms_frontend/bootstrap5/form.html"
