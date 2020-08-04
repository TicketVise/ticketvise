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
from django.urls import path, re_path

#: Contains the url paths for the website.
from django.views.generic import RedirectView

from ticketvise.views.course.labels import CourseLabelsView, CreateCourseLabelView, EditCourseLabelView, \
    DeleteCourseLabelView
from ticketvise.views.course.settings import CourseSettingsView
from ticketvise.views.course.statistics import CourseStatisticsView
from ticketvise.views.course.users import CourseUserDeleteView, CourseUserView, CourseUsersView
from ticketvise.views.courses import CoursesView
from ticketvise.views.error import ErrorHandler
from ticketvise.views.home import HomeView
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
    path("", HomeView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>", TicketView.as_view(), name="ticket"),
    path("courses/<int:course_id>/tickets/new", TicketFormView.as_view(), name="new_ticket"),
    path("courses/<int:course_id>/users/<int:pk>/delete", CourseUserDeleteView.as_view(), name="course_user_delete"),
    path("courses/<int:course_id>/users/<int:pk>", CourseUserView.as_view(), name="course_user"),
    path("courses/<int:pk>/users", CourseUsersView.as_view(), name="course_users"),
    path("courses/<int:pk>/labels", CourseLabelsView.as_view(), name="course_labels"),
    path("courses/<int:pk>/settings", CourseSettingsView.as_view(), name="course_settings"),
    path("courses/<int:pk>/statistics", CourseStatisticsView.as_view(), name="course_statistics"),
    path("courses/<int:pk>/labels/new", CreateCourseLabelView.as_view(), name="create_course_label"),
    path("courses/<int:course_id>/labels/<int:pk>", EditCourseLabelView.as_view(),  name="edit_course_label"),
    path("courses/<int:course_id>/labels/<int:pk>/delete", DeleteCourseLabelView.as_view(), name="delete_course_label"),
    path("courses/<int:course_id>/tickets", TicketOverview.as_view(), name="ticket_overview"),
    path("profile", ProfileView.as_view(), name="profile"),
    path("courses", CoursesView.as_view(), name="courses"),
    path("notifications", NotificationsView.as_view(), name="notifications"),
    path("error/<int:error_code>", ErrorHandler.as_view(), name="error"),
    path(
      "password_reset/",
      auth_views.PasswordResetView.as_view(
          html_email_template_name="registration/password_reset_html_email.html"),
    ),
    path("", include("django.contrib.auth.urls")),
    re_path(r"^api/", include("ticketvise.views.api.urls"))
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handle all the error pages.
for code in [400, 403, 404]:
    vars()[f"handler{code}"] = ErrorHandler.as_view(error_code=code)
