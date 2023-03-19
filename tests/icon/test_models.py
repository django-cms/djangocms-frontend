from django.test import TestCase

from djangocms_frontend.contrib.icon.models import Icon

icon_config = {
    "icon": {
        "libraryId": "zondicons",
        "libraryName": "zondicons",
        "iconHtml": '<i class="zi zi-airplane"></i>',
        "iconMarkup": "&lt;i class=&quot;zi zi-airplane&quot;&gt;&lt;/i&gt;",
        "iconClass": "zi zi-airplane",
        "iconText": "",
        "library": "zondicons",
    },
    "icon_size": "400%",
    "icon_foreground": "primary",
    "icon_rounded": True,
    "attributes": {"color": "black"},
    "background_context": "primary",
    "background_opacity": "50",
    "background_shadow": "reg",
    "responsive_visibility": None,
}


class IconModelTestCase(TestCase):
    def test_icon_instance(self):
        instance = Icon.objects.create(config=icon_config)
        self.assertEqual(str(instance), "Icon (1)")
        self.assertEqual(instance.get_short_description(), "zi zi-airplane")
