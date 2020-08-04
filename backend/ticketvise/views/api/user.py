from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.models.course import Course
from ticketvise.models.user import User
from ticketvise.views.api.security import UserIsCourseStaffMixin


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "avatar_url", "id"]


class UserRoleApiView(UserIsCourseStaffMixin, View):

    def get(self, request, user_id, course_id):
        user = get_object_or_404(User, pk=user_id)
        course = get_object_or_404(Course, pk=course_id)

        role = user.get_role_by_course(course)

        return JsonResponse(role, safe=False)


class CurrentUserApiView(LoginRequiredMixin, RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
