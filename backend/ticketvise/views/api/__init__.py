from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ticketvise.middleware import CurrentUserMiddleware
from ticketvise.models.comment import Comment, CommentHelpful
from ticketvise.models.label import Label
from ticketvise.models.ticket import Ticket, TicketEvent, TicketAttachment, TicketSharedUser
from ticketvise.models.user import User, UserInbox, Role


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
        """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "avatar_url", "id", "is_superuser", "is_active",
                  "give_introduction"]


class TicketSharedUserSerializer(ModelSerializer):
    user = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    sharer = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))

    class Meta:
        model = TicketSharedUser
        fields = ["id", "user", "sharer", "date_created"]


class TicketSerializer(DynamicFieldsModelSerializer):
    """
    Allows data to be converted into Python datatypes for the ticket.
    """
    author = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    shared_with = UserSerializer(read_only=True, many=True,
                                 fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    publish_request_initiator = UserSerializer(fields=(["first_name", "last_name", "avatar_url", "id"]))
    assignee = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    author_role = serializers.SerializerMethodField()
    attachments = serializers.SerializerMethodField()
    shared_with_by = TicketSharedUserSerializer(many=True, read_only=True)
    date_latest_update = serializers.SerializerMethodField()

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

    def get_attachments(self, obj):
        user = CurrentUserMiddleware.get_current_user()

        if user and \
                (user.is_assistant_or_coordinator(obj.inbox) or
                 user.id == obj.author.id or
                 obj.shared_with.filter(id=user.id).exists()):
            return TicketAttachmentSerializer(obj.attachments, many=True, read_only=True).data
        elif obj.is_public:
            return TicketAttachmentSerializer(obj.attachments, fields=["id", "file", "date_created"], many=True, read_only=True).data

        return None

    def get_date_latest_update(self, obj):
        user = CurrentUserMiddleware.get_current_user()
        latest_dates = [obj.date_edited, obj.date_created]

        events = TicketEvent.objects.filter(ticket=obj).values_list("date_edited", flat=True)
        if events:
            latest_dates.append(max(events))

        replies = Comment.objects.filter(ticket=obj, is_reply=True).values_list("date_edited", flat=True)
        if replies:
            latest_dates.append(max(replies))

        if user and user.is_assistant_or_coordinator(obj.inbox):
            comments = Comment.objects.filter(ticket=obj, is_reply=False).values_list("date_edited", flat=True)
            if comments:
                latest_dates.append(max(comments))

        return max(latest_dates)

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
                  "is_pinned", "pin_initiator", "is_public", "publish_request_initiator",
                  "publish_request_created", "is_anonymous", "date_latest_update"]


class CommentSerializer(DynamicFieldsModelSerializer):
    author = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    role = serializers.SerializerMethodField()
    helpful = serializers.SerializerMethodField()

    def get_role(self, obj):
        role = UserInbox.objects.get(user=obj.author, inbox=obj.ticket.inbox).role
        return RoleSerializer(role).data
    
    def get_helpful(self, obj):
        commentHelpful = CommentHelpful.objects.filter(comment=obj)
        return CommentHelpfulSerializer(commentHelpful, many=True).data
        # return 1

    class Meta:
        model = Comment
        fields = ["author", "content", "id", "date_created", "role", "is_approved", "helpful"]
        
        
class CommentHelpfulSerializer(ModelSerializer):
    class Meta:
        model = CommentHelpful
        fields = ["id", "comment", "user", "is_helpful"]


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        fields = ["name", "color", "id", "is_active", "is_visible_to_guest"]


class TicketAttachmentSerializer(DynamicFieldsModelSerializer):
    uploader = UserSerializer(read_only=True, fields=(["first_name", "last_name", "username", "avatar_url", "id"]))
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = TicketAttachment
        fields = ["id", "file", "file_size", "uploader", "date_created"]

    def get_file_size(self, obj):
        return obj.file.size


class RoleSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'key': instance,
            'label': Role[instance].label
        }
