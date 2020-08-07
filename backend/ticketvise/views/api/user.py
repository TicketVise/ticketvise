from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.models.inbox import Inbox
from ticketvise.models.user import User, Role
from ticketvise.views.api.security import UserIsInboxStaffMixin


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "avatar_url", "id"]


class UserRoleApiView(UserIsInboxStaffMixin, View):

    def get(self, request, user_id, inbox_id):
        user = get_object_or_404(User, pk=user_id)
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        role = user.get_role_by_inbox(inbox)
        data = RoleSerializer(role).data

        return JsonResponse(data, safe=False)


class CurrentUserApiView(LoginRequiredMixin, RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RoleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'key': instance,
            'label': Role[instance].label
        }
