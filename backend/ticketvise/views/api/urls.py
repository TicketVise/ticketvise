from django.urls import path

from ticketvise.views.api.comment import TicketCommentsApiView, CreateCommentApiView, CreateReplyApiView, \
    TicketRepliesApiView
from ticketvise.views.api.inbox import InboxStaffApiView, InboxLabelsApiView
from ticketvise.views.api.ticket import TicketApiView, TicketUpdateAssignee, \
    TicketStatusUpdateApiView, \
    RecentTicketApiView, InboxTicketsApiView, TicketLabelApiView, TicketCreateApiView, TicketSharedAPIView
from ticketvise.views.api.user import UserRoleApiView, CurrentUserApiView, UserGetFromUsernameApiView, UsersRolesApiView

urlpatterns = [
    path("inboxes/<int:inbox_id>/tickets", InboxTicketsApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/new", TicketCreateApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>", TicketApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/comments", TicketCommentsApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/comments/post", CreateCommentApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/labels", TicketLabelApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/assignee", TicketUpdateAssignee.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/status", TicketStatusUpdateApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/replies", TicketRepliesApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/replies/post", CreateReplyApiView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/share", TicketSharedAPIView.as_view()),
    path("inboxes/<int:inbox_id>/tickets/<int:ticket_inbox_id>/shared", TicketSharedAPIView.as_view()),
    path("inboxes/<int:inbox_id>/users/<int:user_id>/tickets/recent", RecentTicketApiView.as_view()),
    path("inboxes/<int:inbox_id>/users/<int:user_id>/roles", UsersRolesApiView.as_view()),
    path("inboxes/<int:inbox_id>/role", UserRoleApiView.as_view()),
    path("inboxes/<int:inbox_id>/users/<str:username>", UserGetFromUsernameApiView.as_view()),
    path("inboxes/<int:inbox_id>/staff", InboxStaffApiView.as_view()),
    path("inboxes/<int:inbox_id>/labels", InboxLabelsApiView.as_view()),
    path("me", CurrentUserApiView.as_view()),
]
