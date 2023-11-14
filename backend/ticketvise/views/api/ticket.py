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
import logging
from datetime import datetime
import json

from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.generics import UpdateAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from ticketvise.models.comment import Comment, CommentHelpful
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketAttachment, TicketEvent, Status, TicketStatusEvent, \
    TicketAssigneeEvent, TicketLabelEvent, TicketLabel, TicketTitleEvent
from ticketvise.models.user import User, Role, UserTicket, UserInbox
from ticketvise.notifications import unread_related_ticket_notifications
from ticketvise.models.notification.new import NewTicketNotification
from ticketvise.views.api import CommentSerializer, CommentHelpfulSerializer, TicketSerializer, LabelSerializer
from ticketvise.views.api.inbox import InboxSerializer
from ticketvise.views.api.security import UserIsInInboxPermission, UserIsSuperUserPermission, \
    UserHasAccessToTicketPermission, UserIsInboxStaffPermission, UserIsTicketAuthorOrInboxStaffPermission, \
    UserIsAttachmentUploaderOrInboxStaffPermission
from ticketvise.views.api.user import UserSerializer, UserTicketSerializer


class CreateTicketSerializer(ModelSerializer):
    """
    Allows data to be converted into Python datatypes for the ticket.
    """
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    ticket_inbox_id = serializers.IntegerField(read_only=True)
    make_public = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        """
        Define the model and fields.

        :var Ticket model: The model.
        :var list fields: Field defined to the model.
        """

        #: Tells the serializer to use the :class:`Ticket` model.
        model = Ticket
        #: Tells the serializer to use these fields from the :class:`Ticket` model.
        fields = ["ticket_inbox_id", "title", "content", "labels", "shared_with", "make_public", "is_anonymous"]
        read_only_fields = ["is_public"]

    def validate(self, attrs):
        if not attrs.get("make_public") and attrs.get("is_anonymous"):
            raise ValidationError("An anonymous ticket also needs to be public")
        return attrs

    def validate_shared_with(self, shared_with):
        inbox = self.context["inbox"]
        for user in shared_with:
            if not user.has_inbox(inbox) or user.is_assistant_or_coordinator(inbox):
                raise ValidationError("This ticket cannot be shared with one of these users")
        return shared_with

    def create(self, validated_data):
        if validated_data.pop("make_public"):
            validated_data["is_public"] = datetime.now()

        return super().create(validated_data)
        

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


class PublishRequestUpdateSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["publish_request_initiator", "publish_request_created"]

    def validate_publish_request_initiator(self, initiator):
        inbox = self.instance.inbox
        if not initiator:
            return None
        elif not initiator.is_assistant_or_coordinator(inbox):
            raise ValidationError("You don't have the right permissions to request a publish")
        return initiator


class InboxTicketsApiView(ListAPIView):
    """
    Load the tickets connected to the given :class:`Inbox`.
    """
    permission_classes = [UserIsInInboxPermission]
    page_size = 25

    def get_queryset(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        show_personal = str(self.request.GET.get("show_personal", False)) == "true"
        labels = list(map(int, self.request.GET.getlist("labels[]", [])))
        q = self.request.GET.get("q", "")
        public = json.loads(self.request.GET.get("public", "false"))

        tickets = Ticket.objects.filter(inbox=inbox)
        if q:
            tickets = self.search_tickets(q, inbox)

        if public:
            tickets = tickets.filter(inbox=inbox, is_public__isnull=not public)

        tickets = tickets.order_by("-date_created")

        if not self.request.user.is_assistant_or_coordinator(inbox) and \
                not self.request.user.is_superuser and not public:
            tickets = tickets.filter(author=self.request.user) | \
                      tickets.filter(shared_with__id__exact=self.request.user.id)
        elif show_personal:
            tickets = tickets.filter(assignee=self.request.user) | \
                      tickets.filter(author=self.request.user) | \
                      tickets.filter(assignee=None)

        if labels:
            label_tickets = tickets.filter(labels__id__in=labels)

            # If the "unlabelled" label is selected, then also show the unlabelled tickets.
            if 0 in labels:
                label_tickets = label_tickets | tickets.filter(
                    ~Exists(TicketLabel.objects.filter(ticket__pk=OuterRef("pk")).values_list("id")))

            tickets = label_tickets.distinct()

        return tickets

    def get(self, request, *args, **kwargs):
        """
        Loads the tickets connected to the given inbox.

        :param HttpRequest request: The request.
        :param int id: The id.

        :return:  A list of tickets that are associated with the inbox.
        :rtype: JsonResponse
        """
        inbox = get_object_or_404(Inbox, pk=kwargs["inbox_id"])
        tickets = self.get_queryset()
        status = request.GET.get("status", "")
        page_num = request.GET.get("page", 1)
        public = json.loads(request.GET.get("public", "false"))

        # If no status is given, return the first page of all status
        if not status:
            return self.get_column_tickets(inbox, tickets)

        # Get label from display name
        status = [tag for tag, name in Status.choices if name == status]
        if not status:
            return self.handle_exception(LookupError)

        status = status[0]

        tickets = tickets.filter(status=status)
        paginator = Paginator(tickets, self.page_size)

        page = paginator.page(page_num)

        if public:
            results = TicketSerializer(page.object_list, many=True, fields=(
                "id", "title", "date_created", "labels", "date_latest_update")).data
        else:
            results = TicketSerializer(page.object_list, many=True, fields=(
                "id", "title", "name", "author", "assignee", "ticket_inbox_id", "date_created", "labels",
                "date_latest_update")).data

        return Response({
            "results": results,
            "has_next": page.has_next(),
        })

    def get_column_tickets(self, inbox, query_set):
        """
        Loads the tickets connected to the given inbox
        but divide them into their corresponding column.

        :return: Lists of lists of tickets per status.
        :rtype: QuerySet<:class: `Ticket`>
        """
        columns = [
            {
                "has_next": len(query_set.filter(status=status)) > self.page_size,
                "total": len(query_set.filter(status=status)),
                "page_num": 1,
                "label": status.label,
                "tickets": TicketSerializer(
                    query_set.filter(status=status)[:self.page_size], many=True, fields=(
                        "id", "title", "name", "author", "assignee", "ticket_inbox_id", "date_created", "labels",
                        "date_latest_update", "is_pinned", "is_public")).data
            } for status in Status if status != Status.PENDING
                                      or (inbox.scheduling_algorithm == SchedulingAlgorithm.FIXED
                                          and inbox.fixed_scheduling_assignee is None)
                                      or query_set.filter(status=status).exists()
        ]

        return JsonResponse(data=columns, safe=False)

    def search_tickets(self, q, inbox):
        query = SearchQuery(f"'{q}' & '{q}':*", search_type="raw")

        # Load comments and replies if permissions are right, else load only replies.
        is_reply = [True]
        if self.request.user.is_assistant_or_coordinator(inbox) or self.request.user.is_superuser:
            is_reply = [True, False]

        # Search users
        users = User.objects.annotate(search=SearchVector("first_name", "username", "last_name", "email")).filter(
            search=query, inbox_relationship__inbox=inbox)

        # Search replies
        replies = Comment.objects.annotate(search=SearchVector("content")) \
            .filter(search=query, ticket__inbox=inbox, is_reply__in=is_reply).values("ticket")

        # Search ticket
        tickets = Ticket.objects.annotate(
            search=SearchVector("title", "content", "ticket_inbox_id")).filter(search=query)

        # Combine searches
        tickets = tickets | Ticket.objects.filter(
            Q(author__in=users) | Q(assignee__in=users) | Q(shared_with__in=users) | Q(id__in=replies))

        return tickets


class TicketsApiView(APIView):
    permission_classes = [UserIsSuperUserPermission]

    def get(self, request):
        data = {
            'tickets': Ticket.objects.count()
        }

        return JsonResponse(data, safe=False)


class TicketApiView(RetrieveAPIView):
    permission_classes = [UserHasAccessToTicketPermission]

    def get(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])
        current_role = Role.MANAGER if request.user.is_superuser else request.user.get_entry_by_inbox(inbox).role

        response = {}

        unread_related_ticket_notifications(ticket, request.user)

        if json.loads(request.GET.get("role", "false")):
            response["role"] = current_role

        if json.loads(request.GET.get("ticket", "false")):
            response["ticket"] = TicketSerializer(ticket, fields=(
                "id", "inbox", "title", "ticket_inbox_id", "author", "content", "date_created", "status", "labels",
                "assignee", "attachments", "participants", "author_role", "shared_with_by", "is_pinned",
                "pin_initiator", "shared_with", "is_public", "publish_request_initiator",
                "publish_request_created", "date_latest_update")).data

            # If the ticket is tagged anonymous, remove the author from the data.
            if ticket.is_anonymous:
                response["ticket"]["author"] = None

        if json.loads(request.GET.get("me", "false")):
            user_data = UserSerializer(request.user,
                                       fields=(["first_name", "last_name", "username", "avatar_url", "id",
                                                "is_superuser"])).data
            response["me"] = user_data

        if json.loads(request.GET.get("inbox", "false")):
            inbox_data = InboxSerializer(inbox, fields=("name", "id", "labels")).data
            response["inbox"] = inbox_data

        if json.loads(request.GET.get("replies", "false")):
            replies = Comment.objects.filter(ticket=ticket, is_reply=True).order_by("date_created")
            replies_data = CommentSerializer(replies, many=True).data
            response["replies"] = replies_data

        if json.loads(request.GET.get("events", "false")):
            if self.request.user.is_assistant_or_coordinator(inbox):
                events = TicketEvent.objects.filter(ticket=ticket).select_subclasses()
            else:
                events = TicketEvent.objects.filter(ticket=ticket).exclude(
                    ticketlabelevent__label__is_visible_to_guest=False).select_subclasses()

            events_data = TicketEventSerializer(events, many=True).data
            response["events"] = events_data

        if request.user.is_assistant_or_coordinator(inbox):
            if json.loads(request.GET.get("staff", "false")):
                staff = User.objects.filter(inbox_relationship__role__in=[Role.AGENT, Role.MANAGER],
                                            inbox_relationship__inbox_id=self.kwargs["inbox_id"]) \
                    .values("first_name", "last_name", "username", "avatar_url", "id")

                response["staff"] = staff

            if json.loads(request.GET.get("comments", "false")):
                comments = Comment.objects.filter(ticket=ticket, is_reply=False).order_by("date_created")
                comments_data = CommentSerializer(comments, many=True).data

                response["comments"] = comments_data

        return Response(response)


class UserTicketsApiView(ListAPIView):
    """
    Retrieve every ticket from a user in an inbox.
    """
    serializer_class = TicketSerializer
    permission_classes = [UserIsInboxStaffPermission]

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs["user_id"])
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.filter(author=author, inbox=inbox).order_by("-date_created")


class UserAverageApiView(RetrieveAPIView):
    """
    Return the number of average tickets per inbox for a given user.
    """
    permission_classes = [UserIsInboxStaffPermission]

    def retrieve(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=kwargs["user_id"])

        total = []
        inboxes = UserInbox.objects.filter(user=author)
        for inb in inboxes:
            total.append(Ticket.objects.filter(author=author, inbox=inb.inbox).count())

        if len(total) == 0:
            return Response({ "average": 0 })

        return Response({ "average": sum(total) / len(total) })


class PublicTicketAPIView(RetrieveAPIView):
    permission_classes = [UserIsInInboxPermission]

    def get(self, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])
        response = {}

        if not ticket.is_public:
            raise Http404("No public ticket found with ticket_inbox_id %d", self.kwargs["ticket_inbox_id"])

        if ticket.is_anonymous:
            response["ticket"] = TicketSerializer(ticket, fields=(
                "id", "inbox", "title", "ticket_inbox_id", "content", "date_created", "labels", "participants",
                "attachments", "is_pinned", "pin_initiator")).data
        else:
            response["ticket"] = TicketSerializer(ticket, fields=(
                "id", "inbox", "title", "ticket_inbox_id", "author", "content", "date_created", "labels",
                "participants", "attachments", "author_role", "is_pinned", "pin_initiator")).data

        return Response(response)


class RecentTicketApiView(ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [UserIsInboxStaffPermission]

    def get_queryset(self):
        author = get_object_or_404(User, pk=self.kwargs["user_id"])
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.filter(author=author, inbox=inbox).order_by("-date_created")[:5]


class TicketUpdateAssignee(UpdateAPIView):
    serializer_class = AssigneeUpdateSerializer
    permission_classes = [UserIsInboxStaffPermission]

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketLabelSerializer(ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all())

    class Meta:
        model = Ticket
        fields = ["labels"]


class TicketLabelApiView(UpdateAPIView):
    serializer_class = TicketLabelSerializer
    permission_classes = [UserHasAccessToTicketPermission]

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketAttachmentsApiView(CreateAPIView):
    permission_classes = [UserHasAccessToTicketPermission]

    def get_serializer(self, *args, **kwargs):
        return TicketSerializer(fields="attachments")

    def post(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        for file in self.request.FILES.getlist('files'):
            TicketAttachment(ticket=ticket, file=file).save()

        return Response()


class AttachmentViewApiView(DestroyAPIView):
    permission_classes = [UserIsAttachmentUploaderOrInboxStaffPermission]
    serializer_class = TicketAttachment
    queryset = TicketAttachment


class CloseTicketApiView(APIView):
    permission_classes = [UserIsTicketAuthorOrInboxStaffPermission]

    def patch(self, request, inbox_id, ticket_inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=ticket_inbox_id)

        ticket.status = Status.CLOSED
        ticket.save()

        return Response()


class OpenTicketApiView(APIView):
    permission_classes = [UserIsInboxStaffPermission]

    def patch(self, request, inbox_id, ticket_inbox_id):
        inbox = get_object_or_404(Inbox, pk=inbox_id)
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=ticket_inbox_id)

        ticket.reopen()
        ticket.save()

        return Response()


class TicketCreateApiView(CreateAPIView):
    permission_classes = [UserIsInInboxPermission]
    serializer_class = CreateTicketSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["inbox"] = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return context

    def perform_create(self, serializer):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = serializer.save(author=self.request.user, inbox=inbox)

        # After saving we do the automations so the labels etc. are also created so we can use them in the automations
        try:
            for automation in ticket.inbox.automations.all():
                automation.execute(ticket)

            ticket.save()
        except Exception as e:
            logging.error(e)

        for file in self.request.FILES.getlist('files'):
            TicketAttachment(ticket=ticket, file=file).save()

        if not ticket.assignee:
            for user in ticket.inbox.get_assistants_and_coordinators():
                NewTicketNotification.objects.create(ticket=ticket, receiver=user)


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
    initiator = serializers.SerializerMethodField()
    assignee = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    def get_initiator(self, event):
        if event.initiator and event.initiator.is_assistant_or_coordinator(event.ticket.inbox):
            return UserSerializer(event.initiator, read_only=True,
                                  fields=(["first_name", "last_name", "username", "avatar_url", "id"])).data

        return None

    class Meta:
        model = TicketAssigneeEvent
        fields = ["id", "ticket", "initiator", "date_created", "assignee"]


class TicketLabelEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    label = LabelSerializer(read_only=True)

    class Meta:
        model = TicketLabelEvent
        fields = ["id", "ticket", "initiator", "date_created", "label", "is_added"]


class TicketTitleEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = TicketTitleEvent
        fields = ["id", "ticket", "initiator", "date_created", "old_title", "new_title"]


class TicketEventSerializer(ModelSerializer):
    initiator = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    def to_representation(self, instance):
        if isinstance(instance, TicketStatusEvent):
            return TicketStatusEventSerializer(instance=instance).data
        elif isinstance(instance, TicketAssigneeEvent):
            return TicketAssigneeEventSerializer(instance=instance).data
        elif isinstance(instance, TicketLabelEvent):
            return TicketLabelEventSerializer(instance=instance).data
        elif isinstance(instance, TicketTitleEvent):
            return TicketTitleEventSerializer(instance=instance).data

        return super().to_representation(instance)

    class Meta:
        model = TicketEvent
        fields = "__all__"


class TicketSharedAPIView(UpdateAPIView):
    permission_classes = [UserIsTicketAuthorOrInboxStaffPermission]
    serializer_class = TicketSharedWithUpdateSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketTitleAPIView(UpdateAPIView):
    permission_classes = [UserIsTicketAuthorOrInboxStaffPermission]

    def get_serializer(self, *args, **kwargs):
        return TicketSerializer(fields=["title"], *args, **kwargs)

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])


class TicketPublishAPIView(UpdateAPIView):
    permission_classes = [UserIsTicketAuthorOrInboxStaffPermission]

    def get_serializer(self, *args, **kwargs):
        return TicketSerializer(fields=["is_public", "is_anonymous"], *args, **kwargs)

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

    def update(self, request, *args, **kwargs):
        # Tickets can only be made public, not hidden again.
        ticket = self.get_object()
        ticket.is_public = timezone.now()
        ticket.save()
        return super().update(request, *args, **kwargs)


class TicketPrivateAPIView(UpdateAPIView):
    permission_classes = [UserIsTicketAuthorOrInboxStaffPermission]

    def get_serializer(self, *args, **kwargs):
        return TicketSerializer(fields=["is_public", "is_anonymous"], *args, **kwargs)

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

    def update(self, request, *args, **kwargs):
        # Make a ticket private again.
        ticket = self.get_object()
        ticket.is_public = None
        ticket.publish_request_created = None
        ticket.publish_request_initiator = None
        ticket.save()
        return super().update(request, *args, **kwargs)

class TicketRequestPublishAPIView(UpdateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = PublishRequestUpdateSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.publish_request_created = timezone.now()
        ticket.publish_request_initiator = request.user
        ticket.save()
        return super().update(request, *args, **kwargs)


class PinUnpinTicketAPIView(UpdateAPIView):
    permission_classes = [UserIsInboxStaffPermission]
    serializer_class = TicketSerializer

    def get_serializer(self, *args, **kwargs):
        return TicketSerializer(fields=["is_pinned", "pin_initiator"], *args, **kwargs)

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])

        return Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.is_pinned:
            ticket.is_pinned = None
            ticket.pin_initiator = None
        else:
            ticket.is_pinned = timezone.now()
            ticket.pin_initiator = request.user
        ticket.save()
        return super().update(request, *args, **kwargs)


class HelpfulTicketAPIView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = [UserHasAccessToTicketPermission]
    serializer_class = CommentHelpfulSerializer

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs["ticket_comment_id"])

        return CommentHelpful.objects.get(comment=comment, user=self.request.user)


class SubscribeToTicketAPIView(CreateAPIView):
    permission_classes = [UserHasAccessToTicketPermission]
    serializer_class = UserTicketSerializer

    def create(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = Ticket.objects.get(inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        if ticket in self.request.user.subscribed_tickets.all():
            subscription = UserTicket.objects.get(user=self.request.user, ticket=ticket)
            if subscription.date_removed:
                # User has been subscribed and unsubscribed from ticket,
                # Resubscribe by removing date_removed
                subscription.date_removed = None
                subscription.save()
                serializer = self.get_serializer(subscription)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
            else:
                # User is already subscribed
                self.permission_denied(self.request)

        # Create subscription
        subscription = UserTicket.objects.create(user=self.request.user, ticket=ticket)
        serializer = self.get_serializer(subscription)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UnsubscribeFromTicketAPIView(UpdateAPIView):
    permission_classes = [UserHasAccessToTicketPermission]
    serializer_class = UserTicketSerializer

    def get_object(self):
        inbox = get_object_or_404(Inbox, pk=self.kwargs["inbox_id"])
        ticket = get_object_or_404(Ticket, inbox=inbox, ticket_inbox_id=self.kwargs["ticket_inbox_id"])

        return get_object_or_404(UserTicket, user=self.request.user, ticket=ticket)

    def update(self, request, *args, **kwargs):
        # Remove subscription by setting date_removed, keeping the record.
        subscription = self.get_object()

        subscription.date_removed = timezone.now()
        subscription.save()

        serializer = self.get_serializer(subscription)

        return Response(serializer.data)
