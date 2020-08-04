from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView

from ticketvise import settings
from ticketvise.models.course import Course
from ticketvise.models.label import Label
from ticketvise.views.course.base import LabelCoordinatorRequiredMixin, CourseCoordinatorRequiredMixin


class CourseLabelsView(CourseCoordinatorRequiredMixin, TemplateView):
    template_name = "course/labels.html"

    def get_context_data(self, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs.get("pk"))
        q = self.request.GET.get("q", "")
        page_number = self.request.GET.get('page', '1')

        if not page_number.isnumeric():
            page_number = 1

        labels = Label.objects.filter(course=course, name__icontains=q).order_by("name")
        page = Paginator(labels, settings.PAGE_SIZE).get_page(page_number)

        context = super(TemplateView, self).get_context_data(**kwargs)
        context['course'] = course
        context["index_start"] = (int(page_number) - 1) * settings.PAGE_SIZE + 1
        context["index_end"] = context["index_start"] - 1 + len(page)
        context["total_count"] = labels.count()
        context['labels'] = page

        return context


class EditCourseLabelView(LabelCoordinatorRequiredMixin, UpdateView):
    template_name = "course/label.html"
    model = Label
    fields = ["name", "color", "is_form_label", "is_active"]

    def get_success_url(self):
        return reverse("course_labels", args=(self.kwargs["course_id"],))


class CreateCourseLabelView(CourseCoordinatorRequiredMixin, CreateView):
    template_name = "course/label.html"
    model = Label
    fields = ["name", "color", "is_form_label", "is_active"]

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, pk=self.kwargs["pk"])

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("course_labels", args=(self.kwargs["pk"],))


class DeleteCourseLabelView(LabelCoordinatorRequiredMixin, DeleteView):
    template_name = "course/label.html"
    model = Label

    def get_success_url(self):
        return reverse("course_labels", args=(self.kwargs["course_id"],))
