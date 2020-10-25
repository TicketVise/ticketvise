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
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    DestroyAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketAttachment, TicketEvent, Status, TicketStatusEvent, \
    TicketAssigneeEvent, TicketLabelEvent, TicketLabel, TicketSharedUser
from ticketvise.models.user import User, UserInbox, Role
from ticketvise.views.admin import SuperUserRequiredMixin
from ticketvise.views.api import AUTOCOMPLETE_MAX_ENTRIES, DynamicFieldsModelSerializer
from ticketvise.views.api.comment import CommentSerializer
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.labels import LabelSerializer
from ticketvise.views.api.security import UserHasAccessToTicketMixin, UserIsInboxStaffMixin, UserIsInInboxMixin, \
    UserIsTicketAuthorOrInboxStaffMixin
from ticketvise.views.api.user import UserSerializer, RoleSerializer
from ticketvise.views.notifications import unread_related_ticket_notifications


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
    uploader = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = TicketAttachment
        fields = ["id", "file", "uploader", "date_created"]


class TicketSharedUserSerializer(ModelSerializer):
    user = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    sharer = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = TicketSharedUser
        fields = ["id", "user", "sharer", "date_created"]


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


class TicketSerializer(DynamicFieldsModelSerializer):
    """
    Allows data to be converted into Python datatypes for the ticket.
    """
    author = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    shared_with = UserSerializer(read_only=True, many=True,
                                 fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    assignee = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    author_role = serializers.SerializerMethodField()
    attachments = TicketAttachmentSerializer(many=True, read_only=True)
    shared_with_by = TicketSharedUserSerializer(many=True, read_only=True)

    def get_author_role(self, obj):
        author_role = UserInbox.objects.get(user=obj.author, inbox=obj.inbox).role
        return RoleSerializer(author_role).data

    def get_participants(self, obj):
        participants = list(User.objects.filter(comments__ticket=obj).distinct())

        if obj.author not in participants:
            participants.append(obj.author)

        for user in obj.shared_with.all():
            if user not in participants:
                participants.append(user)

        return UserSerializer(participants, many=True,
                              fields=(["first_name", "last_name", "username", "avatar_url", "id"])).data

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
            return UserSerializer(obj.assignee,
                                  fields=(["first_name", "last_name", "username", "avatar_url", "id"])).data

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
                  "assignee", "shared_with", "participants", "author_role", "attachments", "shared_with_by",
                  "attachments"]


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
        columns = str(request.GET.get("columns", False)) == "true"
        show_personal = str(request.GET.get("show_personal", False)) == "true"
        labels = list(map(int, request.GET.getlist("labels[]", [])))

        inbox = get_object_or_404(Inbox, pk=inbox_id)
        tickets = Ticket.objects.filter(inbox=inbox, title__icontains=q) | \
                  Ticket.objects.filter(inbox=inbox, ticket_inbox_id__icontains=q).order_by("-date_created")

        for term in q.split():
            tickets = tickets | \
                      (Ticket.objects.filter(author__username__icontains=term) |
                       Ticket.objects.filter(author__first_name__icontains=term) |
                       Ticket.objects.filter(author__last_name__icontains=term) |
                       Ticket.objects.filter(author__email__contains=term))

        if not request.user.is_assistant_or_coordinator(inbox) and not request.user.is_superuser:
            tickets = tickets.filter(author=request.user) | tickets.filter(shared_with__id__contains=request.user.id)
        elif show_personal:
            tickets = tickets.filter(assignee=request.user) | \
                      tickets.filter(author=request.user) | \
                      tickets.filter(assignee=None)

        if labels:
            label_tickets = tickets.filter(labels__id__in=labels)

            # If the "unlabelled" label is selected, then also show the unlabelled tickets.
            if 0 in labels:
                label_tickets = label_tickets | tickets.filter(
                    ~Exists(TicketLabel.objects.filter(ticket__pk=OuterRef("pk")).values_list("id")))

            tickets = label_tickets.distinct()

        if columns:
            return self.get_column_tickets(inbox, tickets)

        serializer = TicketSerializer(tickets[:size], many=True, fields=(
            "id", "title", "name", "assignee", "ticket_inbox_id", "date_created", "labels"))
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
                "tickets": TicketSerializer(
                    query_set.filter(status=status)[:25] if status == Status.CLOSED else query_set.filter(
                        status=status), many=True, fields=(
                        "id", "title", "name", "assignee", "ticket_inbox_id", "date_created", "labels")).data
            } for status in Status if status != Status.PENDING
                                      or (inbox.scheduling_algorithm == SchedulingAlgorithm.FIXED
                                          and inbox.fixed_scheduling_assignee is None)
                                      or query_set.filter(status=status).exists()
        ]

        return JsonResponse(data=columns, safe=False)


class TicketsApiView(SuperUserRequiredMixin, APIView):
    def get(self, request):
        data = {
            'tickets': Ticket.objects.count()
        }

        return JsonResponse(data, safe=False)


class TicketApiView(UserHasAccessToTicketMixin, RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        unread_related_ticket_notifications(ticket, request.user)

        current_role = request.user.get_entry_by_inbox(inbox).role

        ticket_data = TicketSerializer(ticket, fields=(
            "id", "inbox", "title", "ticket_inbox_id", "author", "content", "date_created", "status", "labels",
            "assignee", "attachments", "participants", "author_role", "attachments", "shared_with_by",
            "shared_with")).data

        user_data = UserSerializer(request.user,
                                   fields=(["first_name", "last_name", "username", "avatar_url", "id"])).data

        inbox_data = InboxSerializer(inbox).data

        replies = Comment.objects.filter(ticket=ticket, is_reply=True).order_by("date_created")
        replies_data = CommentSerializer(replies, many=True).data

        if self.request.user.is_assistant_or_coordinator(inbox):
            events = TicketEvent.objects.filter(ticket=ticket).select_subclasses()
        else:
            events = TicketEvent.objects.filter(ticket=ticket).exclude(
                ticketlabelevent__label__is_visible_to_guest=False).select_subclasses()

        events_data = TicketEventSerializer(events, many=True).data

        response = {
            "ticket": ticket_data,
            "me": user_data,
            "role": current_role,
            "inbox": inbox_data,
            "replies": replies_data,
            "events": events_data,
        }

        is_staff = current_role == Role.AGENT or current_role == Role.MANAGER or request.user.is_superuser

        if is_staff:
            staff = User.objects.filter(inbox_relationship__role__in=[Role.AGENT, Role.MANAGER],
                                        inbox_relationship__inbox_id=self.kwargs[self.inbox_key]) \
                .values("first_name", "last_name", "username", "avatar_url", "id")

            response["staff"] = staff

            comments = Comment.objects.filter(ticket=ticket, is_reply=False).order_by("date_created")
            comments_data = CommentSerializer(comments, many=True).data

            response["comments"] = comments_data

        return Response(response)


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


class TicketAttachmentsApiView(UserIsTicketAuthorOrInboxStaffMixin, CreateAPIView):
    def get_serializer(self, *args, **kwargs):
        return TicketSerializer(fields="attachments")

    def post(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        for file in self.request.FILES.getlist('files'):
            TicketAttachment(ticket=ticket, file=file).save()

        return Response()


class AttachmentViewApiView(UserIsTicketAuthorOrInboxStaffMixin, DestroyAPIView):
    serializer_class = TicketAttachment
    queryset = TicketAttachment


class CloseTicketApiView(UserIsInboxStaffMixin, APIView):

    def patch(self, request, inbox_id, ticket_inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=ticket_inbox_id)

        ticket.status = Status.CLOSED
        ticket.save()

        return Response()


class OpenTicketApiView(UserIsInboxStaffMixin, APIView):

    def patch(self, request, inbox_id, ticket_inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=ticket_inbox_id)

        ticket.reopen()
        ticket.save()

        return Response()


class TicketCreateApiView(UserIsInInboxMixin, CreateAPIView):
    serializer_class = CreateTicketSerializer

    def perform_create(self, serializer):
        ticket = serializer.save(author=self.request.user)

        for file in self.request.FILES.getlist('files'):
            TicketAttachment(ticket=ticket, file=file).save()


class TicketSharedWithRetrieveSerializer(ModelSerializer):
    shared_with = UserSerializer(many=True, read_only=True,
                                 fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = Ticket
        fields = ["shared_with"]


class TicketSharedWithUpdateSerializer(ModelSerializer):
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Ticket
        fields = ["shared_with"]

    def validate_shared_with(self, shared_with):
        inbox = self.instance.inbox
        for user in shared_with:
            if not user.has_inbox(inbox) or user.is_assistant_or_coordinator(inbox):
                raise ValidationError("This ticket cannot be shared with one of these users")
        return shared_with


class TicketStatusEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = TicketStatusEvent
        fields = ["id", "ticket", "initiator", "date_created", "old_status", "new_status"]


class TicketAssigneeEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    assignee = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = TicketAssigneeEvent
        fields = ["id", "ticket", "initiator", "date_created", "assignee"]


class TicketLabelEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    label = LabelSerializer(read_only=True)

    class Meta:
        model = TicketLabelEvent
        fields = ["id", "ticket", "initiator", "date_created", "label", "is_added"]


class TicketEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

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

        if self.request.user.is_assistant_or_coordinator(inbox):
            return TicketEvent.objects.filter(ticket=ticket).select_subclasses()

        return TicketEvent.objects.filter(ticket=ticket) \
            .exclude(ticketlabelevent__label__is_visible_to_guest=False). \
            select_subclasses()


class TicketSharedAPIView(UserIsTicketAuthorOrInboxStaffMixin, RetrieveUpdateAPIView):

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return TicketSharedWithUpdateSerializer

        return TicketSharedWithRetrieveSerializer
