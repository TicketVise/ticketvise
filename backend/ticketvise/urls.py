"""
Urls
-------------------------------
TicketVise URL configuration, which configures the URL paths for the website.
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path

from ticketvise.views.lti.config import LtiConfigView
from ticketvise.views.lti.lti import LtiView


urlpatterns = [
    path("admin/django", admin.site.urls),
    path("lti", LtiView.as_view()),
    path("lti/config.xml", LtiConfigView.as_view()),
    re_path(r"^api/", include("ticketvise.views.api.urls"))
]
