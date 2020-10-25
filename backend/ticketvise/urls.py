"""
Urls
-------------------------------
TicketVise URL configuration, which configures the URL paths for the website.
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from ticketvise.views.admin import AdminView
from ticketvise.views.error import ErrorHandler
from ticketvise.views.inbox.labels import InboxLabelsView, LabelView, AddInboxLabelView
from ticketvise.views.inbox.overview import InboxView
from ticketvise.views.inbox.settings import InboxSettingsView
from ticketvise.views.inbox.statistics import InboxStatisticsView
from ticketvise.views.inbox.automation import InboxAutomationView
from ticketvise.views.inbox.users import InboxUserDeleteView, InboxUserView, InboxUsersView
from ticketvise.views.inboxes import InboxesView
from ticketvise.views.lti.config import LtiConfigView
from ticketvise.views.lti.lti import LtiView
from ticketvise.views.notifications import NotificationsView
from ticketvise.views.profile import ProfileView
from ticketvise.views.ticket import TicketView
from ticketvise.views.new_ticket import NewTicketView

urlpatterns = [
                  path("admin/django", admin.site.urls),
                  path("admin", AdminView.as_view()),
                  path("lti", LtiView.as_view()),
                  path("lti/config.xml", LtiConfigView.as_view()),
                  path("", InboxesView.as_view(), name="home"),
                  path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>", TicketView.as_view(), name="ticket"),
                  path("inboxes/<int:inbox_id>/tickets/new", NewTicketView.as_view(), name="new_ticket"),
                  path("inboxes/<int:inbox_id>/users/<int:pk>/delete", InboxUserDeleteView.as_view(),
                       name="inbox_user_delete"),
                  path("inboxes/<int:inbox_id>/users/<int:pk>", InboxUserView.as_view(), name="inbox_user"),
                  path("inboxes/<int:pk>/users", InboxUsersView.as_view(), name="inbox_users"),
                  path("inboxes/<int:pk>/labels", InboxLabelsView.as_view(), name="inbox_labels"),
                  path("inboxes/<int:pk>/settings", InboxSettingsView.as_view(), name="inbox_settings"),
                  path("inboxes/<int:pk>/statistics", InboxStatisticsView.as_view(), name="inbox_statistics"),
                  path("inboxes/<int:pk>/automation", InboxAutomationView.as_view(), name="inbox_automation"),
                  path("inboxes/<int:pk>/labels/new", AddInboxLabelView.as_view(), name="create_inbox_label"),
                  path("inboxes/<int:inbox_id>/labels/<int:pk>", LabelView.as_view(), name="edit_inbox_label"),
                  path("inboxes/<int:inbox_id>/tickets", InboxView.as_view(), name="inbox"),
                  path("profile", ProfileView.as_view(), name="profile"),
                  path("inboxes", InboxesView.as_view(), name="inboxes"),
                  path("notifications", NotificationsView.as_view(), name="notifications"),
                  path("error/<int:error_code>", ErrorHandler.as_view(), name="error"),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  re_path(r"^api/", include("ticketvise.views.api.urls"))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handle all the error pages.
for code in [400, 403, 404]:
    vars()[f"handler{code}"] = ErrorHandler.as_view(error_code=code)
