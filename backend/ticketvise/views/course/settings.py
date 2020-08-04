from django.urls import reverse
from django.views.generic import UpdateView

from ticketvise.models.course import Course
from ticketvise.views.course.base import CourseCoordinatorRequiredMixin


class CourseSettingsView(CourseCoordinatorRequiredMixin, UpdateView):
    template_name = "course/settings.html"
    model = Course
    course_key = "pk"
    fields = ["name", "code", "color", "visibility_assignee", "close_answered_weeks",
              "alert_coordinator_unanswered_days", "scheduling_algorithm"]

    def get_success_url(self):
        return reverse("course_settings", args=(self.kwargs["pk"],))
