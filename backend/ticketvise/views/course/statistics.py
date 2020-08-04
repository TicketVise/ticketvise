from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketvise.models.inbox import Course
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import UserCourseRelationship, User
from ticketvise.statistics import get_average_response_time
from ticketvise.views.course.base import CourseCoordinatorRequiredMixin


class CourseStatisticsView(CourseCoordinatorRequiredMixin, TemplateView):
    template_name = "course/statistics.html"

    def get_context_data(self, **kwargs):
        course = get_object_or_404(Course, pk=self.kwargs.get("pk"))

        context = super().get_context_data(**kwargs)

        context['course'] = course
        context['total_tickets'] = Ticket.objects.filter(course=course).count()
        context['total_students'] = UserCourseRelationship.objects.filter(course=course,
                                                                          role=User.Roles.STUDENT).count()
        context['avg_response_time'] = get_average_response_time(course)

        now = datetime.now()
        last_7_days = now - timedelta(days=7)
        context['current_week_pending'] = Ticket.objects.filter(course=course, date_created__gte=last_7_days,
                                                                status=Ticket.Status.PENDING).count()
        context['current_week_assigned'] = Ticket.objects.filter(course=course, date_created__gte=last_7_days,
                                                                 status=Ticket.Status.ASSIGNED).count()
        context['current_week_answered'] = Ticket.objects.filter(course=course, date_created__gte=last_7_days,
                                                                 status=Ticket.Status.ANSWERED).count()
        context['current_week_closed'] = Ticket.objects.filter(course=course, date_created__gte=last_7_days,
                                                               status=Ticket.Status.CLOSED).count()

        last_14_days = now - timedelta(days=14)
        context['last_week_pending'] = Ticket.objects.filter(course=course, date_created__lte=last_7_days,
                                                             date_created__gte=last_14_days,
                                                             status=Ticket.Status.PENDING).count()
        context['last_week_assigned'] = Ticket.objects.filter(course=course, date_created__lte=last_7_days,
                                                              date_created__gte=last_14_days,
                                                              status=Ticket.Status.ASSIGNED).count()
        context['last_week_answered'] = Ticket.objects.filter(course=course, date_created__lte=last_7_days,
                                                              date_created__gte=last_14_days,
                                                              status=Ticket.Status.ANSWERED).count()
        context['last_week_closed'] = Ticket.objects.filter(course=course, date_created__lte=last_7_days,
                                                            date_created__gte=last_14_days,
                                                            status=Ticket.Status.CLOSED).count()

        context['pending_pct'] = calculate_increase(context['current_week_pending'], context['last_week_pending'])
        context['assigned_pct'] = calculate_increase(context['current_week_assigned'], context['last_week_assigned'])
        context['answered_pct'] = calculate_increase(context['current_week_answered'], context['last_week_answered'])
        context['closed_pct'] = calculate_increase(context['current_week_closed'], context['last_week_closed'])

        return context


def calculate_increase(current_week, last_week):
    return round(current_week / last_week, 2) * 100 if last_week else 0

# def get_average_response_time_all_ta(course):
#     return Ticket.objects.filter(course=course, comments__is_reply=True) \
#         .annotate(response_time=F('date_created') - F('comments__date_created')) \
#         .aggregate(avg_response_time=Avg('response_time')) \
#         .values('assignee') \
#         .orderby('response_time')
