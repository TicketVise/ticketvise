from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.serializers import ModelSerializer

from ticketvise.models.comment import Comment
from ticketvise.models.course import Course
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import UserCourseRelationship
from ticketvise.views.api.security import UserHasAccessToTicketMixin, UserIsCourseStaffMixin
from ticketvise.views.api.user import UserSerializer


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        return UserCourseRelationship.objects.get(user=obj.author, course=obj.ticket.course).role

    class Meta:
        model = Comment
        fields = ["author", "content", "id", "date_created", "role"]


class TicketCommentsApiView(UserIsCourseStaffMixin, ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        ticket = get_object_or_404(Ticket, course=course, ticket_course_id=self.kwargs["ticket_course_id"])

        return Comment.objects.filter(ticket=ticket, is_reply=False)


class TicketRepliesApiView(UserHasAccessToTicketMixin, ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        ticket = get_object_or_404(Ticket, course=course, ticket_course_id=self.kwargs["ticket_course_id"])

        return Comment.objects.filter(ticket=ticket, is_reply=True)


class CreateCommentApiView(UserIsCourseStaffMixin, CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs["course_id"]
        ticket_course_id = self.kwargs["ticket_course_id"]
        ticket = get_object_or_404(Ticket, course_id=course_id, ticket_course_id=ticket_course_id)

        serializer.save(ticket=ticket, author=self.request.user, is_reply=False)


class CreateReplyApiView(UserHasAccessToTicketMixin, CreateAPIView):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        course_id = self.kwargs["course_id"]
        ticket_course_id = self.kwargs["ticket_course_id"]
        ticket = get_object_or_404(Ticket, course_id=course_id, ticket_course_id=ticket_course_id)

        serializer.save(ticket=ticket, author=self.request.user, is_reply=True)
