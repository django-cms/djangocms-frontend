from django.urls import include, path

from . import views

app_name = "djangocms_frontend"

urlpatterns = [
    path("link:autocomplete", views.AutocompleteJsonView.as_view(), name="ac_view"),
]

urls = include("djangocms_frontend.contrib.link.urls", namespace="dcf_autocomplete")
