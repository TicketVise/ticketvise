"""
Urls
-------------------------------
TicketVise URL configuration, which configures the URL paths for the website.
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

#: Contains the url paths for the website.
from django.views.generic import RedirectView

from ticketvise.models.label import Label
from ticketvise.models.ticket import TicketLabel, Ticket
from ticketvise.views.inbox.labels import InboxLabelsView, CreateInboxLabelView, EditInboxLabelView, \
    DeleteInboxLabelView
from ticketvise.views.inbox.settings import InboxSettingsView
from ticketvise.views.inbox.statistics import InboxStatisticsView
from ticketvise.views.inbox.users import InboxUserDeleteView, InboxUserView, InboxUsersView
from ticketvise.views.inboxes import InboxesView
from ticketvise.views.error import ErrorHandler
from ticketvise.views.lti.config import LtiConfigView
from ticketvise.views.lti.lti import LtiView
from ticketvise.views.notifications import NotificationsView
from ticketvise.views.profile import ProfileView
from ticketvise.views.settings.lti import LtiSettingsView
from ticketvise.views.ticket import TicketView
from ticketvise.views.ticket_form import TicketFormView
from ticketvise.views.ticket_overview import TicketOverview

urlpatterns = [
    path("admin/", admin.site.urls),
    path("lti", LtiView.as_view()),
    path("lti/config.xml", LtiConfigView.as_view()),
    path("settings/lti", LtiSettingsView.as_view(), name="settings_lti"),
    path("", InboxesView.as_view(), name="home"),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>", TicketView.as_view(), name="ticket"),
    path("inboxes/<int:inbox_id>/tickets/new", TicketFormView.as_view(), name="new_ticket"),
    path("inboxes/<int:inbox_id>/users/<int:pk>/delete", InboxUserDeleteView.as_view(), name="inbox_user_delete"),
    path("inboxes/<int:inbox_id>/users/<int:pk>", InboxUserView.as_view(), name="inbox_user"),
    path("inboxes/<int:pk>/users", InboxUsersView.as_view(), name="inbox_users"),
    path("inboxes/<int:pk>/labels", InboxLabelsView.as_view(), name="inbox_labels"),
    path("inboxes/<int:pk>/settings", InboxSettingsView.as_view(), name="inbox_settings"),
    path("inboxes/<int:pk>/statistics", InboxStatisticsView.as_view(), name="inbox_statistics"),
    path("inboxes/<int:pk>/labels/new", CreateInboxLabelView.as_view(), name="create_inbox_label"),
    path("inboxes/<int:inbox_id>/labels/<int:pk>", EditInboxLabelView.as_view(),  name="edit_inbox_label"),
    path("inboxes/<int:inbox_id>/labels/<int:pk>/delete", DeleteInboxLabelView.as_view(), name="delete_inbox_label"),
    path("inboxes/<int:inbox_id>/tickets", TicketOverview.as_view(), name="ticket_overview"),
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
