from django.urls import path

from ticketvise.views.api.auth import LoginApiView
from ticketvise.views.api.inbox import InboxStaffApiView, InboxLabelApiView, AllInboxLabelsApiView
from ticketvise.views.api.comment import CreateCommentApiView, CreateReplyApiView
from ticketvise.views.api.inbox import InboxLabelsApiView, InboxesApiView, InboxGuestsAPIView, InboxUsersApiView, \
    UserInboxApiView, InboxSettingsApiView, CurrentUserInboxesApiView
from ticketvise.views.api.notification import NotificationsAPIView, NotificationFlipRead, NotificationsReadAll, \
    NotificationUnreadCountAPI
from ticketvise.views.api.statistics import InboxTicketsPerDateTypeStatisticsApiView, \
    InboxAverageAgentResponseTimeStatisticsApiView, InboxAverageTimeToCloseStatisticsApiView, \
    LabelsCountStatisticsApiView, InboxStatisticsApiView
from ticketvise.views.api.ticket import TicketApiView, TicketUpdateAssignee, \
    TicketAttachmentsApiView, AttachmentViewApiView, \
    RecentTicketApiView, InboxTicketsApiView, TicketLabelApiView, TicketCreateApiView, TicketSharedAPIView, \
    TicketsApiView, OpenTicketApiView, CloseTicketApiView
from ticketvise.views.api.user import UserRoleApiView, CurrentUserApiView, NotificationsSettingsAPIView, \
    UserGetFromUsernameApiView, UsersApiView

urlpatterns = [
    path("login", LoginApiView.as_view()),
    path("inboxes", InboxesApiView.as_view()),
    path("inboxes/<int:inbox_id>/settings", InboxSettingsApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets", InboxTicketsApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/new", TicketCreateApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>", TicketApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/attachments", TicketAttachmentsApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/attachments/<int:pk>", AttachmentViewApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/comments/post", CreateCommentApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/labels", TicketLabelApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/assignee", TicketUpdateAssignee.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/status/open", OpenTicketApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/status/close", CloseTicketApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/replies/post", CreateReplyApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/shared", TicketSharedAPIView.as_view()),
    path("inboxes/<int:inbox_id>/users/<int:user_id>/tickets/recent", RecentTicketApiView.as_view()),
    path("inboxes/<int:inbox_id>/role", UserRoleApiView.as_view()),
    path("inboxes/<int:inbox_id>/guests", InboxGuestsAPIView.as_view()),
    path("inboxes/<int:inbox_id>/users", InboxUsersApiView.as_view()),
    path("inboxes/<int:inbox_id>/users/<int:user_id>", UserInboxApiView.as_view()),
    path("inboxes/<int:inbox_id>/users/<str:username>", UserGetFromUsernameApiView.as_view()),
    path("inboxes/<int:inbox_id>/labels", InboxLabelsApiView.as_view()),
    path("inboxes/<int:inbox_id>/staff", InboxStaffApiView.as_view()),
    path("inboxes/<int:inbox_id>/labels", InboxLabelsApiView.as_view(), name="api_inbox_labels"),
    path("inboxes/<int:inbox_id>/labels/all", AllInboxLabelsApiView.as_view(), name="api_all_inbox_labels"),
    path("inboxes/<int:inbox_id>/labels/new", InboxLabelsApiView.as_view(), name="api_new_inbox_label"),
    path("inboxes/<int:inbox_id>/labels/<int:label_id>", InboxLabelApiView.as_view(), name="api_inbox_label"),
    path("inboxes/<int:inbox_id>/statistics", InboxStatisticsApiView.as_view()),
    path("inboxes/<int:inbox_id>/statistics/tickets/count", InboxTicketsPerDateTypeStatisticsApiView.as_view()),
    path("inboxes/<int:inbox_id>/statistics/agent/response/avg",
         InboxAverageAgentResponseTimeStatisticsApiView.as_view()),
    path("inboxes/<int:inbox_id>/statistics/close/avg", InboxAverageTimeToCloseStatisticsApiView.as_view()),
    path("inboxes/<int:inbox_id>/statistics/labels/count", LabelsCountStatisticsApiView.as_view()),
    path("admin/statistics/users/count", UsersApiView.as_view()),
    path("admin/statistics/tickets/count", TicketsApiView.as_view()),
    path("notifications", NotificationsAPIView.as_view()),
    path("notifications/unread", NotificationUnreadCountAPI.as_view()),
    path("notifications/read/all", NotificationsReadAll.as_view()),
    path("notifications/<int:pk>/read", NotificationFlipRead.as_view()),
    path("me", CurrentUserApiView.as_view()),
    path("me/settings", NotificationsSettingsAPIView.as_view()),
    path("me/inboxes", CurrentUserInboxesApiView.as_view()),
]
