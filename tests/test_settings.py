import os

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.messages",
    "easy_thumbnails",
    "filer",
    "cms",
    "menus",
    "treebeard",
    "djangocms_text",
    "djangocms_link",
    "djangocms_frontend",
    "djangocms_frontend.contrib.accordion",
    "djangocms_frontend.contrib.alert",
    "djangocms_frontend.contrib.badge",
    "djangocms_frontend.contrib.card",
    "djangocms_frontend.contrib.carousel",
    "djangocms_frontend.contrib.collapse",
    "djangocms_frontend.contrib.content",
    "djangocms_frontend.contrib.grid",
    "djangocms_frontend.contrib.icon",
    "djangocms_frontend.contrib.image",
    "djangocms_frontend.contrib.jumbotron",
    "djangocms_frontend.contrib.link",
    "djangocms_frontend.contrib.listgroup",
    "djangocms_frontend.contrib.media",
    "djangocms_frontend.contrib.navigation",
    "djangocms_frontend.contrib.tabs",
    "djangocms_frontend.contrib.utilities",
    "sekizai",
    "tests.test_app",
]

try:  # V4 test?
    import djangocms_versioning  # noqa

    INSTALLED_APPS += [
        "djangocms_versioning",
    ]
except ImportError:  # Nope
    pass

try:  # url manager test?
    import djangocms_url_manager  # noqa

    INSTALLED_APPS += [
        "djangocms_url_manager",
    ]
except ImportError:  # Nope
    pass

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "cms.middleware.user.CurrentUserMiddleware",
    "cms.middleware.page.CurrentPageMiddleware",
    "cms.middleware.toolbar.ToolbarMiddleware",
    "cms.middleware.language.LanguageCookieMiddleware",
]
CMS_LANGUAGES = {
    1: [
        {
            "code": "en",
            "name": "English",
        }
    ]
}

# required otherwise subject_location would throw an error in the template
THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

LANGUAGE_CODE = "en"
ALLOWED_HOSTS = ["localhost"]
DJANGOCMS_PICTURE_RESPONSIVE_IMAGES = False
DJANGOCMS_PICTURE_RESPONSIVE_IMAGES_VIEWPORT_BREAKPOINTS = [576, 768, 992]

SECRET_KEY = "fake-key"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(os.path.dirname(__file__), "templates"),
            # insert your TEMPLATE_DIRS here
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",  # This is where you put the name of the db file.
        # If one doesn't exist, it will be created at migration time.
    }
}

CMS_TEMPLATES = (("page.html", "Page"),)

SITE_ID = 1

STATIC_URL = "/static/"

ROOT_URLCONF = "tests.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CMS_CONFIRM_VERSION4 = True  # Needed for v4, neglected in v3

TEXT_SAVE_IMAGE_FUNCTION = "djangocms_frontend.contrib.image.image_save.create_image_plugin"

CMS_COMPONENT_PLUGINS = [
    "djangocms_frontend.cms_plugins.CMSUIPlugin",
    "djangocms_frontend.cms_plugins.AutoHeroPlugin",
    "TextPlugin",
]
