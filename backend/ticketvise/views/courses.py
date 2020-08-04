"""
Courses
-------------------------------
Contains the view for the courses overview.

**Table of contents**

* :class:`CoursesView`
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from ticketvise.models.inbox import Course
from ticketvise.models.user import UserCourseRelationship


class BookmarkCourseForm(ModelForm):
    class Meta:
        """
        Define the model and fields.

        :var UserCourseRelationship model: The model.
        :var list fields: Fields defined to the model.
        """

        model = UserCourseRelationship
        fields = ["is_bookmarked"]


class CoursesView(LoginRequiredMixin, TemplateView):
    """
    Display all the courses for a user.

    :var str template_name: The name of the template to be rendered.
    :var User user: The user visiting the page.
    :var QuerySet<:class: `Course`> courses: The courses to display.
    :var int num_courses: The total number of courses.
    :var int tiles_per_row: The amount of tiles in a row.
    :var int num_tiles_needed: The amount of empty tiles to get formatting nice.
    """

    template_name = "courses.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # entries = UserCourseRelationship.objects.filter(user=self.user).order_by("-is_bookmarked").values("course")
        # course_ids = list(map(lambda entry: entry["course"], entries))
        context["courses"] = Course.objects.filter(user_relationship__user=self.request.user).order_by(
            "-user_relationship__is_bookmarked")
        context['tiles_per_row'] = 3
        context['num_tiles_needed'] = context['tiles_per_row'] - context["courses"].count() % context['tiles_per_row']
        context['extra_tiles_list'] = list(range(context['num_tiles_needed']))

        return context
    #
    # def dispatch(self, request, *args, **kwargs):
    #     """
    #     Set the variables to display content from the database on the webpage.
    #
    #     :param HttpRequest request: The request.
    #     :param list args: Additional list arguments.
    #     :param dict kwargs: Additional keyword arguments.
    #
    #     :return: None.
    #     """
    #     self.courses = request.user.courses.all()
    #     self.num_courses = self.courses.count()
    #
    #     # The number of extra tiles needed to make sure that every row of tiles contains 3 tiles.
    #     self.tiles_per_row = 3
    #     self.num_tiles_needed = self.tiles_per_row - self.num_courses % self.tiles_per_row
    #     self.extra_tiles_list = list(range(self.num_tiles_needed))
    #
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        if request.POST["course_id"]:
            course = Course.objects.get(pk=request.POST["course_id"])
            if not request.user.has_course(course):
                raise ValueError(f"User is not assigned to or enrolled in course {course}")

            relation = request.user.get_entry_by_course(course)
            relation.is_bookmarked = not relation.is_bookmarked
            relation.save()

        return HttpResponseRedirect(reverse("courses"))
