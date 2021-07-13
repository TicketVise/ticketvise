"""
Urls
-------------------------------
TicketVise URL configuration, which configures the URL paths for the website.
"""
import private_storage.urls
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView

from ticketvise.views.error import ErrorHandler
from ticketvise.views.lti.config import LtiConfigView
from ticketvise.views.lti.lti import LtiView


class IndexView(TemplateView):
    template_name = "index.html"


urlpatterns = [
                  path("admin/django", admin.site.urls),
                  path("lti", LtiView.as_view()),
                  path("lti/config.xml", LtiConfigView.as_view()),
                  path("", IndexView.as_view(), name="home"),
                  path("error/<int:error_code>", ErrorHandler.as_view(), name="error"),
                  path('^private-media/', include(private_storage.urls)),
                  re_path(r"^api/", include("ticketvise.views.api.urls"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handle all the error pages.
for code in [400, 403, 404]:
    vars()[f"handler{code}"] = ErrorHandler.as_view(error_code=code)
