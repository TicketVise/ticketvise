"""
Urls
-------------------------------
TicketVise URL configuration, which configures the URL paths for the website.
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path

# from ticketvise.views.lti.config import LtiConfigView
# from ticketvise.views.lti.lti import LtiView
from ticketvise.views.lti.lti import LTILoginView
from ticketvise.views.lti.lti import LTILaunchView


urlpatterns = [
    path("api/admin/django", admin.site.urls),
    path("lti/login", LTILoginView),
    path("lti/launch", LTILaunchView),
    re_path(r"^api/", include("ticketvise.views.api.urls"))
]
