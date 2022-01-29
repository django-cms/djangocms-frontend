#!/usr/bin/env python
HELPER_SETTINGS = {
    "INSTALLED_APPS": [
        "easy_thumbnails",
        "filer",
        "mptt",
        "djangocms_text_ckeditor",
        "djangocms_link",
        "djangocms_picture",
        "djangocms_frontend",
        "djangocms_frontend.contrib.alert",
        "djangocms_frontend.contrib.badge",
        "djangocms_frontend.contrib.card",
        "djangocms_frontend.contrib.carousel",
        "djangocms_frontend.contrib.collapse",
        "djangocms_frontend.contrib.content",
        "djangocms_frontend.contrib.grid",
        "djangocms_frontend.contrib.jumbotron",
        "djangocms_frontend.contrib.link",
        "djangocms_frontend.contrib.listgroup",
        "djangocms_frontend.contrib.media",
        "djangocms_frontend.contrib.image",
        "djangocms_frontend.contrib.tabs",
        "djangocms_frontend.contrib.utilities",
    ],
    "CMS_LANGUAGES": {
        1: [
            {
                "code": "en",
                "name": "English",
            }
        ]
    },
    # required otherwise subject_location would throw an error in the template
    "THUMBNAIL_PROCESSORS": (
        "easy_thumbnails.processors.colorspace",
        "easy_thumbnails.processors.autocrop",
        "filer.thumbnail_processors.scale_and_crop_with_subject_location",
        "easy_thumbnails.processors.filters",
    ),
    "LANGUAGE_CODE": "en",
    "ALLOWED_HOSTS": ["localhost"],
    "DJANGOCMS_PICTURE_RESPONSIVE_IMAGES": False,
    "DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS": [576, 768, 992],
}


def run():
    from app_helper import runner

    runner.cms("djangocms_frontend")


if __name__ == "__main__":
    run()
