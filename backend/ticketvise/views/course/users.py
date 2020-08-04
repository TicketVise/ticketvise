from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, DeleteView

from ticketvise import settings
from ticketvise.models.course import Course
from ticketvise.models.user import User, UserCourseRelationship
from ticketvise.views.course.base import CourseCoordinatorRequiredMixin, UserCoordinatorRequiredMixin


class CourseUsersView(CourseCoordinatorRequiredMixin, TemplateView):
    template_name = "course/users.html"

    def get_context_data(self, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs.get("pk"))

        if not self.request.user.is_coordinator_for_course(course):
            raise PermissionDenied()

        q = self.request.GET.get("q", "")
        page_number = self.request.GET.get('page', '1')

        if not page_number.isnumeric():
            page_number = 1

        users = (User.objects.filter(courses=course, username__icontains=q)
                 | User.objects.filter(courses=course, first_name__icontains=q)
                 | User.objects.filter(courses=course, last_name__icontains=q)
                 | User.objects.filter(courses=course, email__contains=q)).order_by("first_name")

        context = super(TemplateView, self).get_context_data(**kwargs)

        page = Paginator(users, settings.PAGE_SIZE).get_page(page_number)

        context['course'] = course
        context["index_start"] = (int(page_number) - 1) * settings.PAGE_SIZE + 1
        context["index_end"] = context["index_start"] - 1 + len(page)
        context["total_count"] = users.count()
        context['users'] = page

        return context


class CourseUserView(UserCoordinatorRequiredMixin, UpdateView):
    template_name = "course/user.html"
    model = UserCourseRelationship
    fields = ["role"]

    def get_object(self, queryset=None):
        return UserCourseRelationship.objects.get(user__id=self.kwargs.get("pk"),
                                                  course_id=self.kwargs.get("course_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        context["course"] = get_object_or_404(Course, pk=self.kwargs["course_id"])

        return context

    def get_success_url(self):
        return reverse("course_users", args=(self.kwargs["course_id"],))


class CourseUserDeleteView(UserCoordinatorRequiredMixin, DeleteView):
    template_name = "course/user.html"
    model = UserCourseRelationship

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = get_object_or_404(User, pk=self.kwargs["pk"])
        context["course"] = get_object_or_404(Course, pk=self.kwargs["course_id"])

        return context

    def get_object(self, queryset=None):
        return UserCourseRelationship.objects.get(user__id=self.kwargs["pk"],
                                                  course__id=self.kwargs["course_id"])

    def get_success_url(self):
        return reverse("course_users", args=(self.kwargs["course_id"],))
