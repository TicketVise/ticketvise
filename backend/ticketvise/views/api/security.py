from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from ticketvise.models.inbox import Course
from ticketvise.models.ticket import Ticket


class UserIsInCourseMixin(AccessMixin):
    course_key = "course_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        course_id = kwargs.get(self.course_key)
        if not course_id:
            return self.handle_no_permission()

        course = get_object_or_404(Course, pk=course_id)
        if not request.user.has_course(course) and not request.user.is_assistant_or_coordinator(course):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserIsCourseStaffMixin(AccessMixin):
    course_key = "course_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        course_id = kwargs.get(self.course_key)
        if not course_id:
            return self.handle_no_permission()

        course = get_object_or_404(Course, pk=course_id)
        if not request.user.is_assistant_or_coordinator(course):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserHasAccessToTicketMixin(AccessMixin):
    course_key = "course_id"
    ticket_key = "ticket_course_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        course_id = kwargs.get(self.course_key)
        if not course_id:
            return self.handle_no_permission()

        ticket_course_id = kwargs.get(self.ticket_key)
        if not ticket_course_id:
            return self.handle_no_permission()

        ticket = get_object_or_404(Ticket, course_id=course_id, ticket_course_id=ticket_course_id)
        if not (request.user.id == ticket.author.id or request.user.is_assistant_or_coordinator(ticket.course)):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
