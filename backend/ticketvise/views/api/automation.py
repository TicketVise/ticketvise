import json
from typing import DefaultDict
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from application.backend.ticketvise import models
from application.backend.ticketvise.models import automation
from ticketvise.models.automation import Automation, AutomationCondition
from ticketvise.views.api.inbox import InboxSerializer

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
from ticketvise.views.api import CommentSerializer, DynamicFieldsModelSerializer
from ticketvise.views.api.security import UserIsInboxStaffPermission, UserHasAccessToTicketPermission

import itertools

# class Automation(models.Model):
#     name = models.CharField(max_length=255)
#     inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="automation_condition")
#     action_func = models.CharField(max_length=50)
#     action_value = models.CharField(max_length=50)

# class AutomationCondition(models.Model):

#     automation = models.ForeignKey("Automation", on_delete=models.CASCADE)
#     field_name = models.CharField(max_length=50)
#     evaluation_func = models.CharField(max_length=50, choices=EVALUATION_FUNC_CHOICES)
#     evaluation_value = models.CharField(max_length

class AutomationSerializer(DynamicFieldsModelSerializer):
    # inbox = InboxSerializer(fields=["name", "id", "color", "labels", "image", "code", "coordinator"])
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    labels = models.OneTo("Label", blank=True, related_name="tickets", through="TicketLabel")

    class Meta:
        model = Automation
        fields = ["name", "action_func", "action_value"]

class AutomationConditionSerializer(DynamicFieldsModelSerializer):
    automation = AutomationSerializer(read_only=True, fields=(["name", "action_func", "action_value"]))

    class Meta:
        model = AutomationCondition
        fields = ["automation", "field_name", "evaluation_func", "evaluation_value"]


class ListCreateAutomationApiView(ListCreateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationSerializer

    def perform_create(self, serializer):
        inbox_id = self.kwargs["inbox_id"]
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        serializer.save(inbox=inbox)

    def list(self, request, *args, **kwargs):
        inbox_id = self.kwargs["inbox_id"]
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        conditions = AutomationCondition.objects.filter(automation__inbox=inbox)
        results = DefaultDict(list)
        for condition in conditions:
            data = AutomationConditionSerializer(condition).data
            results[condition.automation.id].append(data)
        
        return JsonResponse(results, safe=False)

class CreateAutomationConditionApiView(CreateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationConditionSerializer

    def perform_create(self, serializer):
        inbox_id = self.kwargs["inbox_id"]
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        serializer.save(inbox=inbox)


class AutomationApiView(RetrieveUpdateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationSerializer

    def get_object(self):
        inbox_id = self.kwargs["inbox_id"]
        automation_id = self.kwargs["automation_id"]
        return get_object_or_404(Automation, pk=automation_id, inbox__id=inbox_id)

    def update(self, request, *args, **kwargs):
        inbox_id = self.kwargs["inbox_id"]
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        conditions = AutomationCondition.objects.filter(automation__inbox=inbox)
        results = DefaultDict(list)
        for condition in conditions:
            data = AutomationConditionSerializer(condition).data
            results[condition.automation.id].append(data)
        
        return JsonResponse(results, safe=False)

    def delete(self, request, *args, **kwargs):
        inbox_id = self.kwargs["inbox_id"]
        automation_id = self.kwargs["automation_id"]
        automation = get_object_or_404(Automation, pk=automation_id, inbox__id=inbox_id)

        automation.delete()

        return Response(status=204)
