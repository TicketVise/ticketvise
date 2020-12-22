from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.models.inbox import Inbox
from ticketvise.models.notification import Notification
from ticketvise.models.user import User, Role, UserInbox
from ticketvise.views.admin import SuperUserRequiredMixin
from ticketvise.views.api import DynamicFieldsModelSerializer
from ticketvise.views.api.security import UserIsInInboxPermission


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "avatar_url", "id", "is_superuser", "is_active"]


class UserInboxSerializer(ModelSerializer):
    user = UserSerializer(
        fields=("first_name", "last_name", "email", "username", "avatar_url", "id", "is_superuser", "is_active"))
    role_label = serializers.SerializerMethodField()

    def get_role_label(self, user_inbox):
        return Role[user_inbox.role].label

    class Meta:
        model = UserInbox
        fields = ["id", "role", "role_label", "user", "is_bookmarked", "is_assignable"]


class UserNotificationSettingsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "notification_mention_mail",
            "notification_mention_app",
            "notification_new_ticket_mail",
            "notification_new_ticket_app",
            "notification_comment_mail",
            "notification_comment_app",
            "notification_assigned_mail",
            "notification_assigned_app",
            "notification_ticket_reminder_mail",
            "notification_ticket_reminder_app"
        ]


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ["receiver", "read"]


class UserUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "avatar_url", "id"]


class UserRoleApiView(APIView):
    permission_classes = [UserIsInInboxPermission]

    def get(self, request, inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        # A superuser hasn't got any role inside an inbox.
        if self.request.user.is_superuser:
            return JsonResponse({}, safe=False)

        role = self.request.user.get_role_by_inbox(inbox)
        data = RoleSerializer(role).data

        return JsonResponse(data, safe=False)


class UserGetFromUsernameApiView(RetrieveUpdateAPIView):
    permission_classes = [UserIsInInboxPermission]
    serializer_class = UserUsernameSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        user = get_object_or_404(User, username=self.kwargs["username"])

        if not user.has_inbox(inbox) or user.is_assistant_or_coordinator(inbox):
            self.handle_exception(Http404)

        return user

    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return JsonResponse({"username": ["Username not found within this inbox"]}, status=404)
        return super().handle_exception(exc)


class CurrentUserApiView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RoleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'key': instance,
            'label': Role[instance].label
        }


class NotificationsSettingsAPIView(RetrieveUpdateAPIView):
    serializer_class = UserNotificationSettingsSerializer

    def get_object(self):
        return self.request.user


class UsersApiView(SuperUserRequiredMixin, View):
    def get(self, request):
        data = {
            'users': User.objects.count()
        }

        return JsonResponse(data, safe=False)
