from djangocms_frontend.models import FrontendUIItem


class Form(FrontendUIItem):
    class Meta:
        proxy = True
