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
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.models.inbox import Inbox
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketAttachment
from ticketvise.models.user import User, UserInbox
from ticketvise.views.api import AUTOCOMPLETE_MAX_ENTRIES
from ticketvise.views.api.security import UserHasAccessToTicketMixin, UserIsInboxStaffMixin, UserIsInInboxMixin
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
    assignee = UserSerializer(many=False, read_only=True)
    labels = LabelSerializer(many=True, read_only=True)

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

    shared_with = UserSerializer(many=True, read_only=True)

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
        participants.append(obj.author)

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
        if not assignee.is_assistant_or_coordinator(inbox):
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
            inbox=inbox, ticket_inbox_id__icontains=q)

        if not request.user.is_assistant_or_coordinator(inbox):
            tickets = tickets.filter(author=request.user)
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
            } for status in Ticket.Status
        ]

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
