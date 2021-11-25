from collections import defaultdict
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.response import Response
from ticketvise.models.automation import Automation, AutomationCondition

from ticketvise.models.inbox import Inbox
from ticketvise.views.api import DynamicFieldsModelSerializer
from ticketvise.views.api.security import UserIsInboxStaffPermission


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

    class Meta:
        model = Automation
        fields = ["name", "action_func", "action_value"]


class AutomationConditionSerializer(DynamicFieldsModelSerializer):
    automation = AutomationSerializer(read_only=True, fields=(["name", "action_func", "action_value"]))

    class Meta:
        model = AutomationCondition
        fields = ["automation", "field_name", "evaluation_func", "evaluation_value"]


# class ListCreateAutomationApiView(ListCreateAPIView):
#     permission_classes = [UserIsInboxStaffPermission]
#     serializer_class = AutomationSerializer
#
#     def perform_create(self, serializer):
#         inbox_id = self.kwargs["inbox_id"]
#         inbox = get_object_or_404(Inbox, pk=inbox_id)
#
#         serializer.save(inbox=inbox)
#
#     def list(self, request, *args, **kwargs):
#         inbox_id = self.kwargs["inbox_id"]
#         inbox = get_object_or_404(Inbox, pk=inbox_id)
#
#         conditions = AutomationCondition.objects.filter(automation__inbox=inbox)
#         results = defaultdict(list)
#         for condition in conditions:
#             data = AutomationConditionSerializer(condition).data
#             results[condition.automation.id].append(data)
#
#         return JsonResponse(results, safe=False)

class ListAutomationApiView(ListAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationSerializer
    lookup_url_kwarg = "inbox_id"


class CreateAutomationConditionApiView(CreateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationConditionSerializer

    def perform_create(self, serializer):
        automation_id = self.kwargs["automation_id"]
        automation = get_object_or_404(Automation, pk=automation_id)

        serializer.save(automation=automation)


class AutomationConditionApiView(RetrieveUpdateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationConditionSerializer


class AutomationApiView(RetrieveUpdateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationSerializer

    def get_object(self):
        inbox_id = self.kwargs["inbox_id"]
        automation_id = self.kwargs["automation_id"]
        return get_object_or_404(Automation, pk=automation_id, inbox__id=inbox_id)

    def get(self, request, *args, **kwargs):
        conditions = AutomationCondition.objects.filter(automation=self.get_object())
        results = defaultdict(list)

        for condition in conditions:
            data = AutomationConditionSerializer(condition).data
            results[automation].append(data)

        return JsonResponse(results, safe=False)

    def delete(self, request, *args, **kwargs):
        inbox_id = self.kwargs["inbox_id"]
        automation_id = self.kwargs["automation_id"]
        automation = get_object_or_404(Automation, pk=automation_id, inbox__id=inbox_id)

        automation.delete()

        return Response(status=204)


class CreateAutomationApiView(CreateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = AutomationSerializer

    def perform_create(self, serializer):
        inbox_id = self.kwargs["inbox_id"]
        inbox = get_object_or_404(Inbox, pk=inbox_id)

        serializer.save(inbox=inbox)
