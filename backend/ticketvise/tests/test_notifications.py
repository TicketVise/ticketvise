"""
Test Notifications
-------------------------------
This file tests the notification functionality on the website.
"""
from urllib.parse import urlencode

from django.forms import model_to_dict
from django.test import TestCase, Client

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.models.notification import Notification
from ticketvise.models.notification.assigned import TicketAssignedNotification
from ticketvise.models.notification.comment import CommentNotification
from ticketvise.models.notification.mention import MentionNotification
from ticketvise.models.notification.new import NewTicketNotification
from ticketvise.models.notification.reminder import TicketReminderNotification
from ticketvise.models.ticket import Ticket
from ticketvise.models.user import User, Role


class NotificationsTestCase(TestCase):
    def setUp(self):
        """
        Setup for each of these tests.
        We create a client and also a dummy test user.

        :return: None.
        """
        self.client = Client()
        self.inbox = Inbox.objects.create(code="ABC", name="how to code",
                                          scheduling_algorithm=SchedulingAlgorithm.MANUAL)

        self.student = User.objects.create_user(
            username="student", email="student@ticketvise.com", password="test12345", is_staff=False,
        )
        self.student.add_inbox(self.inbox)

        self.ta = User.objects.create_user(
            username="admin", email="admin@ticketvise.com", password="test67891", is_staff=True,
        )
        self.ta.add_inbox(self.inbox, Role.AGENT)

        self.ta2 = User.objects.create_user(
            username="admin2", email="admin2@ticketvise.com", password="test67891", is_staff=True
        )
        self.ta2.add_inbox(self.inbox, Role.AGENT)

        self.ticket = Ticket.objects.create(author=self.student, assignee=self.ta,
                                            title="How to code?",
                                            inbox=self.inbox, content="wat is 1+1?")
        self.ticket_2 = Ticket.objects.create(author=self.student, assignee=self.ta,
                                              title="How to code v2?",
                                              inbox=self.inbox, content="wat is 2+1?")
        self.ticket_unassigned = Ticket.objects.create(author=self.student,
                                                       title="How to code v2?",
                                                       inbox=self.inbox, content="wat is 2+1?")

    def test_notification_page_200(self):
        """
        Authorized users should see the notification page.

        :return: None.
        """
        self.client.force_login(self.student)
        response = self.client.get("/notifications")
        self.assertEqual(response.status_code, 200)

    def test_notification_page_401(self):
        """
        Unauthorized users should be redirected to the login page. When logged in
        it should redirect to the notification page.

        :return: None.
        """
        response = self.client.get("/notifications")
        self.assertRedirects(response, "/login/?next=/notifications")

    def test_assigned_ticket(self):
        """
        If There is an assignee of a ticket, they must receive the notification.

        :return: None.
        """
        self.client.force_login(self.ta)

        self.ticket.assignee = None
        self.ticket.save()

        self.ticket.assignee = self.ta
        self.ticket.save()

        exists = TicketAssignedNotification.objects.filter(ticket=self.ticket, receiver=self.ta).exists()
        self.assertTrue(exists)

    def test_unassigned_ticket(self):
        """
        If a ticket has no assignee, all TA"s connected to a inbox must receive a notification.

        :return: None.
        """
        self.client.force_login(self.ta)

        self.ticket.inbox.scheduling_algorithm = SchedulingAlgorithm.MANUAL
        self.ticket.inbox.save()

        ticket = Ticket.objects.create(author=self.student, assignee=None, title="How to code v3?", inbox=self.inbox,
                                       content="wat is 3+1?")

        for user in self.ticket.inbox.get_assistants_and_coordinators():
            exists = NewTicketNotification.objects.filter(ticket=ticket, receiver=user).exists()
            self.assertTrue(exists)

    def test_mark_notification_read_toggle(self):
        """
        A user must be able to mark notifications as unread.

        :return: None.
        """
        self.client.force_login(self.ta)
        notification = Notification.objects.create(receiver=self.ta)

        self.client.post("/notifications", urlencode({"id": notification.id}), follow=True,
                         content_type="application/x-www-form-urlencoded")
        self.assertTrue(Notification.objects.get(pk=notification.id).is_read)

        self.client.post("/notifications", urlencode({"id": notification.id}), follow=True,
                         content_type="application/x-www-form-urlencoded")
        self.assertFalse(Notification.objects.get(pk=notification.id).is_read)

    def test_mark_all_notifications_read(self):
        """
        A user must be able to mark all notifications as unread at once.

        :return: None.
        """
        self.client.force_login(self.ta)

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertFalse(notification.is_read)

        self.client.post("/notifications", follow=True)

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertTrue(notification.is_read)

    def test_opening_ticket_marks_related_notifications_as_read(self):
        """
        If a link to a ticket from notifications is clicked, the notification must be marked as
        read.

        :return: None.
        """
        self.client.force_login(self.ta)

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertFalse(notification.is_read)

        self.client.get("/inboxes/{}/tickets/{}".format(self.ticket.inbox.id,
                                                        self.ticket.ticket_inbox_id),
                        follow=True)

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertTrue(notification.is_read)

    def test_mention_notification(self):
        """
        If a user is mentioned, it needs to receive a notification.

        :return: None.
        """
        self.client.force_login(self.ta2)
        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="@admin")

        self.assertTrue(MentionNotification.objects.filter(receiver=self.ta,
                                                           comment__ticket=self.ticket).exists())

    def test_mention_invalid_username_notification(self):
        self.assertTrue(bool(Comment._username_regex.search("@tom")))
        self.assertFalse(bool(Comment._username_regex.search("tom@uva.nl")))
        self.assertTrue(bool(Comment._username_regex.search("    @tom  ")))
        self.assertTrue(bool(Comment._username_regex.search("    @tom")))
        self.assertTrue(bool(Comment._username_regex.search("@tom  ")))
        self.assertTrue(bool(Comment._username_regex.search("@@@tom")))
        self.assertTrue(bool(Comment._username_regex.search("@tom@")))

    def test_comment_visibility_student(self):
        """
        If a comment is placed under a ticket, the student author should not get a notification.
        If a reply is placed under a ticket, the studen author should get a notification.

        :return: None.
        """
        self.client.force_login(self.student)

        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test", is_reply=False)

        self.assertFalse(CommentNotification.objects.filter(receiver=self.student).exists())

        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test", is_reply=True)

        self.assertTrue(CommentNotification.objects.filter(receiver=self.student).exists())

    def test_notification_settings_form(self):
        """
        If a comment is placed under a ticket, the student author should not get a notification.
        If a reply is placed under a ticket, the studen author should get a notification.

        :return: None.
        """
        self.client.force_login(self.ta)

        settings = ["notification_mention_mail",
                    "notification_mention_app",
                    "notification_ticket_status_change_mail",
                    "notification_ticket_status_change_app",
                    "notification_new_ticket_mail",
                    "notification_new_ticket_app",
                    "notification_comment_mail",
                    "notification_comment_app"]

        for setting in settings:
            for b in [False, True]:
                data = dict.fromkeys(settings, True)
                data["action"] = "notifications"
                data[setting] = b

                self.client.post("/profile", urlencode(data), follow=True,
                                 content_type="application/x-www-form-urlencoded")
                user_dict = model_to_dict(User.objects.get(username="admin"))

                self.assertEqual(user_dict[setting], b)

    def test_disabled_mention_notification(self):
        """
        If a user has disabled notifications, he should not receive any
        notifications in the notification panel.

        :return: None.
        """
        self.client.force_login(self.ta)

        MentionNotification.objects.all().delete()
        CommentNotification.objects.all().delete()
        Notification.objects.all().delete()

        settings = ["notification_mention_mail",
                    "notification_mention_app",
                    "notification_ticket_status_change_mail",
                    "notification_ticket_status_change_app",
                    "notification_new_ticket_mail",
                    "notification_new_ticket_app",
                    "notification_comment_mail",
                    "notification_comment_app"]

        data = dict.fromkeys(settings, False)
        data["action"] = "notifications"

        self.client.post("/profile", urlencode(data), follow=True,
                         content_type="application/x-www-form-urlencoded")

        no_notifications_ticket = Ticket.objects.create(author=self.student,
                                                        title="How to code v2?",
                                                        inbox=self.inbox, content="wat is 2+1?")
        comment = Comment.objects.create(ticket=no_notifications_ticket, author=self.ta2,
                                         content="@admin")

        receiver = User.objects.get(pk=self.ta.id)
        MentionNotification(receiver=receiver, comment=comment).save()
        self.assertFalse(MentionNotification.objects.filter(receiver=receiver).exists())

        CommentNotification(receiver=receiver, comment=comment).save()
        self.assertFalse(CommentNotification.objects.filter(receiver=receiver).exists())

    def test_getters_comment_notifications(self):
        """
        Test all getters of the CommentNotifications.

        :return: None.
        """
        reply = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)
        comment_notification = CommentNotification.objects.create(comment=reply, receiver=self.ta)
        self.assertEqual(comment_notification.ticket, reply.ticket)
        self.assertEqual(comment_notification.author, f"@{reply.author.username}")
        self.assertEqual(comment_notification.content, f"{reply.author.get_full_name()} has posted a reply")
        self.assertEqual(comment_notification.inbox, self.ticket.inbox)

        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=False)
        comment_notification = CommentNotification.objects.create(comment=comment, receiver=self.ta)
        self.assertEqual(comment_notification.content, f"{comment.author.get_full_name()} has posted a comment")

    def test_getters_mention_notifications(self):
        """
        Test all getters of the MentionNotifications.

        :return: None.
        """
        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)
        mention_notification = MentionNotification.objects.create(comment=comment, receiver=self.ta)
        self.assertEqual(mention_notification.ticket, comment.ticket)
        self.assertEqual(mention_notification.author, f"@{comment.author.username}")
        self.assertEqual(mention_notification.content,
                         f"You have been mentioned by {comment.author.get_full_name()}")
        self.assertEqual(mention_notification.inbox, self.ticket.inbox)

    def test_notification_getters_not_implemented(self):
        """
        Test the notification funcitonality when there are no getters.

        :return: None.
        """
        notification = Notification.objects.create(receiver=self.ta)
        with self.assertRaises(NotImplementedError):
            notification.author
        with self.assertRaises(NotImplementedError):
            notification.content
        with self.assertRaises(NotImplementedError):
            notification.inbox


class NotificationsAPITestCase(NotificationsTestCase):

    def test_get_notifications_200(self):
        self.client.force_login(self.student)
        response = self.client.get("/api/notifications")
        self.assertEqual(response.status_code, 200)

    def test_get_notifications_unauthorized(self):
        response = self.client.get("/api/notifications")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/api/notifications")

    def test_get_notifications_read_all(self):
        self.client.force_login(self.ta)

        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)

        notifications = [
            MentionNotification.objects.create(receiver=self.ta, is_read=False, comment=comment),
            CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=comment),
            TicketAssignedNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)
        ]

        response = self.client.put("/api/notifications/read/all")
        self.assertEqual(response.status_code, 200)

        for notification in notifications:
            self.assertTrue(Notification.objects.get(pk=notification.id).is_read)

    def test_get_notifications_flip_read(self):
        self.client.force_login(self.ta)

        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)

        notifications = [
            MentionNotification.objects.create(receiver=self.ta, is_read=False, comment=comment),
            CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=comment),
            TicketAssignedNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)
        ]

        for notification in notifications:
            response = self.client.put(f"/api/notifications/{notification.id}/read")
            self.assertEqual(response.status_code, 200)
            self.assertTrue(Notification.objects.get(pk=notification.id).is_read)

        for notification in notifications:
            response = self.client.put(f"/api/notifications/{notification.id}/read")
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Notification.objects.get(pk=notification.id).is_read)
