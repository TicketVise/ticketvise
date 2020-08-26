"""
API
-------------------------------
Contains classes for the API interface to dynamically load models using AJAX.

**Table of contents**

* :class:`UserSerializer`
* :class:`TicketSerializer`
* :class:`InboxUsersView`
* :class:`InboxTicketView`
"""

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketAttachment, TicketEvent, Status, TicketStatusEvent, \
    TicketAssigneeEvent, TicketLabelEvent
from ticketvise.models.user import User, UserInbox
from ticketvise.views.api import AUTOCOMPLETE_MAX_ENTRIES
from ticketvise.views.api.security import UserHasAccessToTicketMixin, UserIsInboxStaffMixin, UserIsInInboxMixin, \
    UserIsTicketAuthorOrInboxStaffMixin
from ticketvise.views.api.user import UserSerializer, RoleSerializer


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ["name", "color", "id"]


class TicketSerializer(ModelSerializer):
    """
    Allows data to be converted into Python datatypes for the ticket.
    """
    author = UserSerializer(read_only=True)
    assignee = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    def get_labels(self, obj):
        user = CurrentUserMiddleware.get_current_user()
        labels = obj.labels.filter(is_active=True)
        if user and not user.is_assistant_or_coordinator(obj.inbox):
            labels = labels.filter(is_visible_to_guest=True)
            return LabelSerializer(labels, many=True, read_only=True).data
        return LabelSerializer(labels, many=True, read_only=True).data

    def get_assignee(self, obj):
        user = CurrentUserMiddleware.get_current_user()

        if user and (user.is_assistant_or_coordinator(obj.inbox) or obj.inbox.show_assignee_to_guest):
            return UserSerializer(obj.assignee).data

        return None

    class Meta:
        """
        Define the model and fields.

        :var Ticket model: The model.
        :var list fields: Field defined to the model.
        """

        #: Tells the serializer to use the :class:`Ticket` model.
        model = Ticket
        #: Tells the serializer to use these fields from the :class:`Ticket` model.
        fields = ["id", "inbox", "title", "ticket_inbox_id", "author", "content", "date_created", "status", "labels",
                  "assignee", "shared_with"]


class CreateTicketSerializer(ModelSerializer):
    """
    Allows data to be converted into Python datatypes for the ticket.
    """
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        """
        Define the model and fields.

        :var Ticket model: The model.
        :var list fields: Field defined to the model.
        """

        #: Tells the serializer to use the :class:`Ticket` model.
        model = Ticket
        #: Tells the serializer to use these fields from the :class:`Ticket` model.
        fields = ["inbox", "title", "content", "labels", "shared_with"]

    def validate_shared_with(self, shared_with):
        inbox = get_object_or_404(Inbox, pk=int(self.get_initial()["inbox"]))
        for user in shared_with:
            if not user.has_inbox(inbox) or user.is_assistant_or_coordinator(inbox):
                raise ValidationError("This ticket cannot be shared with one of these users")
        return shared_with


class TicketAttachmentSerializer(ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ["file"]


class TicketWithParticipantsSerializer(TicketSerializer):
    """
    Allows data to be converted into Python datatypes for the ticket.
    """
    participants = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    attachments = TicketAttachmentSerializer(many=True, read_only=True)

    def get_role(self, obj):
        role = UserInbox.objects.get(user=obj.author, inbox=obj.inbox).role
        return RoleSerializer(role).data

    def get_participants(self, obj):
        participants = list(User.objects.filter(comments__ticket=obj).distinct())

        if obj.author not in participants:
            participants.append(obj.author)

        for user in obj.shared_with.all():
            if user not in participants:
                participants.append(user)

        return UserSerializer(participants, many=True).data

    class Meta:
        model = Ticket
        fields = ["id", "inbox", "title", "ticket_inbox_id", "author", "content", "date_created", "status", "labels",
                  "assignee", "attachments", "participants", "role", "attachments"]


class AssigneeUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["assignee"]

    def validate_assignee(self, assignee):
        inbox = self.instance.inbox
        if not assignee:
            return None
        elif not assignee.is_assistant_or_coordinator(inbox):
            raise ValidationError("User doesn't have the right permissions to be assigned to this ticket")
        return assignee


class InboxTicketsApiView(UserIsInInboxMixin, APIView):
    """
    Load the tickets connected to the given :class:`Inbox`.
    """

    def get(self, request, inbox_id):
        """
        Loads the tickets connected to the given inbox.

        :param HttpRequest request: The request.
        :param int id: The id.

        :return:  A list of tickets that are associated with the inbox.
        :rtype: JsonResponse
        """
        q = request.GET.get("q", "")
        size = int(request.GET.get("size", AUTOCOMPLETE_MAX_ENTRIES))
        columns = bool(request.GET.get("columns", False))
        show_personal = str(request.GET.get("show_personal", False)) == "true"
        labels = list(map(int, request.GET.getlist("labels[]", [])))

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        tickets = Ticket.objects.filter(inbox=inbox, title__icontains=q) | Ticket.objects.filter(
            inbox=inbox, ticket_inbox_id__icontains=q).order_by("-date_created")

        if not request.user.is_assistant_or_coordinator(inbox):
            tickets = tickets.filter(author=request.user) | tickets.filter(shared_with__id__icontains=request.user.id)
        elif show_personal:
            tickets = tickets.filter(assignee=request.user) | tickets.filter(author=request.user)

        if labels:
            tickets = tickets.filter(labels__id__in=labels).distinct()

        if columns:
            return self.get_column_tickets(inbox, tickets)

        serializer = TicketSerializer(tickets[:size], many=True)
        return JsonResponse(serializer.data, safe=False)

    def get_column_tickets(self, inbox, query_set):
        """
        Loads the tickets connected to the given inbox
        but divide them into their corresponding column.

        :return: Lists of lists of tickets per status.
        :rtype: QuerySet<:class: `Ticket`>
        """
        columns = [
            {
                "label": status.label,
                "tickets": TicketSerializer(query_set.filter(status=status), many=True).data
            } for status in Status
        ]

        if not self.request.user.is_assistant_or_coordinator(inbox) \
                and not inbox.show_assignee_to_guest:
            columns[0] = {
                "label": columns[0]["label"],
                "tickets": columns[0]["tickets"] + columns[1]["tickets"]
            }
            del columns[1]
        columns[0]["tickets"] = sorted(columns[0]["tickets"], key=lambda x: x["date_created"], reverse=True)

        return JsonResponse(data=columns, safe=False)


class TicketApiView(UserHasAccessToTicketMixin, RetrieveAPIView):
    serializer_class = TicketWithParticipantsSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class RecentTicketApiView(UserIsInboxStaffMixin, ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs["user_id"])
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.filter(author=author, inbox=inbox).order_by("-date_created")[:5]


class TicketUpdateAssignee(UserIsInboxStaffMixin, UpdateAPIView):
    serializer_class = AssigneeUpdateSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketLabelSerializer(ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())

    class Meta:
        model = Ticket
        fields = ["labels"]


class TicketLabelApiView(UserIsInboxStaffMixin, UpdateAPIView):
    serializer_class = TicketLabelSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketStatusUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["status"]


class TicketStatusUpdateApiView(UserIsInboxStaffMixin, UpdateAPIView):
    serializer_class = TicketStatusUpdateSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketCreateApiView(UserIsInInboxMixin, CreateAPIView):
    serializer_class = CreateTicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save(author=self.request.user)

        for file in self.request.FILES.getlist('files'):
            TicketAttachment(ticket=ticket, file=file).save()


class TicketSharedWithRetrieveSerializer(ModelSerializer):
    shared_with = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["shared_with"]

    def validate_shared_with(self, shared_with):
        inbox = self.instance.inbox
        for user in shared_with:
            if not user.has_inbox(inbox) or user.is_assistant_or_coordinator(inbox):
                raise ValidationError("This ticket cannot be shared with one of these users")
        return shared_with


class TicketSharedWithUpdateSerializer(ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Ticket
        fields = ["shared_with"]


class TicketStatusEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True)

    class Meta:
        model = TicketStatusEvent
        fields = ["ticket", "initiator", "date_created", "status"]


class TicketAssigneeEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = TicketAssigneeEvent
        fields = ["ticket", "initiator", "date_created", "assignee"]


class TicketLabelEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True)
    label = LabelSerializer(read_only=True)

    class Meta:
        model = TicketLabelEvent
        fields = ["ticket", "initiator", "date_created", "label", "is_added"]


class TicketEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True)

    def to_representation(self, instance):
        if isinstance(instance, TicketStatusEvent):
            return TicketStatusEventSerializer(instance=instance).data
        elif isinstance(instance, TicketAssigneeEvent):
            return TicketAssigneeEventSerializer(instance=instance).data
        elif isinstance(instance, TicketLabelEvent):
            return TicketLabelEventSerializer(instance=instance).data

        return super().to_representation(instance)

    class Meta:
        model = TicketEvent
        fields = "__all__"


class TicketEventsApiView(UserHasAccessToTicketMixin, ListAPIView):
    serializer_class = TicketEventSerializer

    def get_queryset(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        return TicketEvent.objects.filter(ticket=ticket).select_subclasses()


class TicketSharedAPIView(UserIsTicketAuthorOrInboxStaffMixin, RetrieveUpdateAPIView):
    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return TicketSharedWithUpdateSerializer

        return TicketSharedWithRetrieveSerializer
