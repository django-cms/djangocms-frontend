from django import forms
from djangocms_link.fields import LinkFormField

from djangocms_frontend.component_base import CMSFrontendComponent
from djangocms_frontend.component_pool import components
from djangocms_frontend.contrib.image.fields import ImageFormField


@components.register
class MyHero(CMSFrontendComponent):
    class Meta:
        # declare plugin properties
        name = "My Hero Component"
        render_template = "hero.html"
        allow_children = True
        mixins = ["Background"]
        slots = (
            ("title", "Title"),
            ("slot", "Slot"),
        )
        # for more complex components, you can add fieldsets

    # declare fields
    title = forms.CharField(required=True, initial="my title")
    slogan = forms.CharField(required=True, initial="django CMS' plugins are great components", widget=forms.Textarea)
    image = ImageFormField(required=True)

    # add description for the structure board
    def get_short_description(self):
        return self.title


@components.register
class MyButton(CMSFrontendComponent):
    class Meta:
        name = "Button"
        render_template = "button.html"
        allow_children = False

    text = forms.CharField(required=True, initial="Click me")
    link = LinkFormField()

    def get_short_description(self):
        return self.text


@components.register
class MyStrangeComponent(CMSFrontendComponent):
    text = forms.CharField(required=True, initial="Message")
