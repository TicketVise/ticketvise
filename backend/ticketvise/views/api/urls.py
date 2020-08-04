from django.urls import path

from ticketvise.views.api.comment import TicketCommentsApiView, CreateCommentApiView, CreateReplyApiView, \
    TicketRepliesApiView
from ticketvise.views.api.course import CourseStaffApiView, CourseLabelsApiView
from ticketvise.views.api.ticket import TicketApiView, TicketUpdateAssignee, \
    TicketStatusUpdateApiView, \
    RecentTicketApiView, CourseTicketsApiView, TicketLabelApiView, TicketCreateApiView
from ticketvise.views.api.user import UserRoleApiView, CurrentUserApiView

urlpatterns = [
    path("courses/<int:course_id>/tickets", CourseTicketsApiView.as_view()),
    path("courses/<int:course_id>/tickets/new", TicketCreateApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>", TicketApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/comments", TicketCommentsApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/comments/post", CreateCommentApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/labels", TicketLabelApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/assignee", TicketUpdateAssignee.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/status", TicketStatusUpdateApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/replies", TicketRepliesApiView.as_view()),
    path("courses/<int:course_id>/tickets/<int:ticket_course_id>/replies/post", CreateReplyApiView.as_view()),
    path("courses/<int:course_id>/users/<int:user_id>/tickets/recent", RecentTicketApiView.as_view()),
    path("courses/<int:course_id>/users/<int:user_id>/roles", UserRoleApiView.as_view()),
    path("courses/<int:course_id>/staff", CourseStaffApiView.as_view()),
    path("courses/<int:course_id>/labels", CourseLabelsApiView.as_view()),
    path("me", CurrentUserApiView.as_view()),
]
