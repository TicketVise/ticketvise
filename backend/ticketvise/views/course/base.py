from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from ticketvise.models.inbox import Course
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import UserCourseRelationship


class CourseCoordinatorRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is the course coordinator.
    """
    course_key = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        course_id = kwargs.get(self.course_key)
        if not course_id:
            return self.handle_no_permission()

        course = get_object_or_404(Course, pk=course_id)
        if not request.user.is_coordinator_for_course(course):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class CourseStaffRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is staff of the course.
    """
    ticket_key = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        ticket_id = kwargs.get(self.ticket_key)
        if not ticket_id:
            return self.handle_no_permission()
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        course = get_object_or_404(Course, pk=ticket.course.id)
        if not request.user.is_assistant_or_coordinator(course):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class LabelCoordinatorRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is the coordinator of the course in which the label exists.
    """
    label_key = "pk"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        label_id = kwargs.get(self.label_key)
        if not label_id:
            return self.handle_no_permission()

        label = get_object_or_404(Label, pk=label_id)
        if not request.user.is_coordinator_for_course(label.course):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class UserCoordinatorRequiredMixin(AccessMixin):
    """
    Mixin to verify that the user accessing the view is the coordinator of the course in which the targeted user is
    associated with.
    """
    user_key = "pk"
    course_key = "course_id"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        user_id = kwargs.get(self.user_key)
        if not user_id:
            return self.handle_no_permission()

        course_id = kwargs.get(self.course_key)
        if not course_id:
            return self.handle_no_permission()

        user_course = get_object_or_404(UserCourseRelationship, user__id=user_id, course__id=course_id)
        if not request.user.is_coordinator_for_course(user_course.course):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
