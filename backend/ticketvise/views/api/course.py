from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView

from ticketvise.models.inbox import Course
from ticketvise.models.label import Label
from ticketvise.models.user import User
from ticketvise.views.api.security import UserIsCourseStaffMixin, UserIsInCourseMixin
from ticketvise.views.api.ticket import LabelSerializer
from ticketvise.views.api.user import UserSerializer


class CourseStaffApiView(UserIsCourseStaffMixin, ListAPIView):
    serializer_class = UserSerializer
    staff_roles = [User.Roles.ASSISTANT, User.Roles.COORDINATOR]

    def get_queryset(self):
        return User.objects.filter(course_relationship__role__in=self.staff_roles,
                                   course_relationship__course_id=self.kwargs[self.course_key])


class CourseLabelsApiView(UserIsInCourseMixin, ListAPIView):
    serializer_class = LabelSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs[self.course_key])
        return Label.objects.filter(course=course).order_by("name")
