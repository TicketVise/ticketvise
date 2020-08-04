"""
Test Notifications
-------------------------------
This file tests the notification functionality on the website.
"""
from urllib.parse import urlencode

from django.forms import model_to_dict
from django.test import TestCase, Client
from django.urls import reverse

from ticketvise.models.comment import Comment
from ticketvise.models.inbox import Inbox
from ticketvise.models.notification import Notification, MentionNotification, CommentNotification
from ticketvise.models.ticket import Ticket, TicketStatusChangedNotification
from ticketvise.models.user import User


class NotificationsTestCase(TestCase):
    def setUp(self):
        """
        Setup for each of these tests.
        We create a client and also a dummy test user.

        :return: None.
        """
        self.client = Client()
        self.inbox = Inbox.objects.create(code="ABC", name="how to code")

        self.student = User.objects.create_user(
            username="student", email="root@ticketvise.com", password="test12345", is_staff=False,
        )
        self.student.inboxes.add(self.inbox)
        self.student.set_password("test12345")
        self.student.save()

        self.ta = User.objects.create_user(
            username="admin", email="admin@ticketvise.com", password="test67891", is_staff=True
        )
        self.ta.add_inbox(self.inbox, User.Roles.ASSISTANT)
        self.ta.set_password("test67891")
        self.ta.save()

        self.ta2 = User.objects.create_user(
            username="admin2", email="admin2@ticketvise.com", password="test67891", is_staff=True
        )
        self.ta2.add_inbox(self.inbox, User.Roles.ASSISTANT)
        self.ta2.set_password("test67891")
        self.ta2.save()

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
        self.client.login(username="student", password="test12345")
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

    def test_new_ticket_notification(self):
        """
        When a new ticket is created, TA"s registered to the inbox, or the assigned TA should
        receive a notification.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")

        ticket_notification = TicketStatusChangedNotification.objects.filter(
            receiver=self.ta, old_status=None, ticket__assignee__isnull=False).exists()
        self.assertTrue(ticket_notification)

        ticket_notification = TicketStatusChangedNotification.objects.filter(
            receiver=self.ta, old_status=None, ticket__assignee__isnull=True).exists()
        self.assertTrue(ticket_notification)

    def test_status_changed_notification(self):
        """
        When the status of a ticket is changed, a notification must be sent.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")
        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test comment for "
                                                                            "status change",
                               is_reply=True, is_active=True)

        Comment.objects.create(ticket=self.ticket_2, author=self.ta2, content="test comment for "
                                                                              "status change",
                               is_reply=True, is_active=True)

        status_change_notification = TicketStatusChangedNotification.objects.filter(
            receiver=self.ta, old_status=None).exists()
        self.assertTrue(status_change_notification)

    def test_unchanged_ticket_status(self):
        """
        When a ticket is updated, but the status remains the same, no notification must be sent.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")
        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test comment for "
                                                                            "status change",
                               is_reply=True, is_active=True)

        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test comment for "
                                                                            "status change",
                               is_reply=True, is_active=True)

        status_change_notifications = TicketStatusChangedNotification.objects.filter(
            receiver=self.ta)
        for status_change_notification in status_change_notifications:
            self.assertFalse(status_change_notification.old_status ==
                             status_change_notification.new_status)

    def test_assigned_ticket(self):
        """
        If There is an assignee of a ticket, they must receive the notification.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")

        ticket_notification = TicketStatusChangedNotification.objects.filter(
            ticket__assignee=self.ta, receiver=self.ta).exists()
        self.assertTrue(ticket_notification)

    def test_unassigned_ticket(self):
        """
        If a ticket has no assignee, all TA"s connected to a inbox must receive a notification.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")

        ticket_notification = TicketStatusChangedNotification.objects.filter(
            ticket__assignee=None, receiver=self.ta).exists()
        self.assertTrue(ticket_notification)

        Ticket.objects.create(author=self.student, assignee=None,
                              title="How to code v3?",
                              inbox=self.inbox, content="wat is 3+1?")

        ticket_notification = TicketStatusChangedNotification.objects.filter(
            ticket__assignee=None, receiver=self.ta).exists()
        self.assertTrue(ticket_notification)

    def test_mark_notification_read_toggle(self):
        """
        A user must be able to mark notifications as unread.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")
        notification = Notification.objects.filter(read=False).first()

        self.client.post("/notifications", urlencode({"id": notification.id}), follow=True,
                         content_type="application/x-www-form-urlencoded")
        self.assertTrue(Notification.objects.get(pk=notification.id).read)

        self.client.post("/notifications", urlencode({"id": notification.id}), follow=True,
                         content_type="application/x-www-form-urlencoded")
        self.assertFalse(Notification.objects.get(pk=notification.id).read)

    def test_mark_all_notifications_read(self):
        """
        A user must be able to mark all notifications as unread at once.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")


        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertFalse(notification.read)

        self.client.post("/notifications", follow=True)

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertTrue(notification.read)

    def test_opening_ticket_marks_related_notifications_as_read(self):
        """
        If a link to a ticket from notifications is clicked, the notification must be marked as
        read.

        :return: None.
        """
        self.client.login(username="admin", password="test67891")

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertFalse(notification.read)

        self.client.get("/inboxes/{}/tickets/{}".format(self.ticket.inbox.id,
                                                        self.ticket.ticket_inbox_id),
                        follow=True)

        for notification in Notification.objects.filter(receiver=self.ticket.author):
            self.assertTrue(notification.read)

    def test_mention_notification(self):
        """
        If a user is mentioned, it needs to receive a notification.

        :return: None.
        """
        self.client.login(username="admin2", password="test67891")
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
        self.client.login(username="student", password="test12345")

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
        self.client.login(username="admin", password="test67891")

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
        self.client.login(username="admin", password="test67891")

        MentionNotification.objects.all().delete()
        CommentNotification.objects.all().delete()
        TicketStatusChangedNotification.objects.all().delete()
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

        TicketStatusChangedNotification(receiver=receiver, ticket=no_notifications_ticket,
                                        new_status="Closed",
                                        old_status="Pending").save()
        self.assertFalse(
            TicketStatusChangedNotification.objects.filter(receiver=receiver).exists())

    def test_getters_comment_notifications(self):
        """
        Test all getters of the CommentNotifications.

        :return: None.
        """
        reply = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)
        comment_notification = CommentNotification.objects.create(comment=reply, receiver=self.ta)
        self.assertEqual(comment_notification.get_ticket_url(),
                         reverse("ticket", args=[reply.ticket.inbox.id, reply.ticket.ticket_inbox_id]))
        self.assertEqual(comment_notification.get_title(), reply.ticket.title)
        self.assertEqual(comment_notification.get_author(), f"@{reply.author.username}")
        self.assertEqual(comment_notification.get_content(), f"{reply.author.get_full_name()} has posted a reply")
        self.assertEqual(comment_notification.get_inbox(), self.ticket.inbox)

        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=False)
        comment_notification = CommentNotification.objects.create(comment=comment, receiver=self.ta)
        self.assertEqual(comment_notification.get_content(), f"{comment.author.get_full_name()} has posted a comment")

    def test_getters_mention_notifications(self):
        """
        Test all getters of the MentionNotifications.

        :return: None.
        """
        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)
        mention_notification = MentionNotification.objects.create(comment=comment, receiver=self.ta)
        self.assertEqual(mention_notification.get_ticket_url(),
                         reverse("ticket", args=[comment.ticket.inbox.id, comment.ticket.ticket_inbox_id]))
        self.assertEqual(mention_notification.get_title(), comment.ticket.title)
        self.assertEqual(mention_notification.get_author(), f"@{comment.author.username}")
        self.assertEqual(mention_notification.get_content(),
                         f"You have been mentioned by {comment.author.get_full_name()}")
        self.assertEqual(mention_notification.get_inbox(), self.ticket.inbox)

    def test_getters_ticket_status_change(self):
        """
        Test all getters of the TicketStatusChangeNotifications.

        :return: None.
        """
        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)
        ticket_status_change = TicketStatusChangedNotification.objects.create(ticket=self.ticket, old_status="Pending",
                                                                              new_status="Closed", receiver=self.ta)
        self.assertEqual(ticket_status_change.get_ticket_url(),
                         reverse("ticket", args=[comment.ticket.inbox.id, comment.ticket.ticket_inbox_id]))
        self.assertEqual(ticket_status_change.get_title(), self.ticket.title)
        self.assertEqual(ticket_status_change.get_author(), f"@{self.ticket.author.username}")
        self.assertEqual(ticket_status_change.get_content(),
                         f"Ticket status changed from \"{ticket_status_change.old_status}\" to "
                         f"\"{ticket_status_change.new_status}\"")
        self.assertEqual(ticket_status_change.get_inbox(), self.ticket.inbox)

        ticket_status_change = TicketStatusChangedNotification.objects.create(ticket=self.ticket, new_status="Pending",
                                                                              receiver=self.ta)
        self.assertEqual(ticket_status_change.get_content(), "A new ticket has been opened")

    def test_notification_getters_not_implemented(self):
        """
        Test the notification funcitonality when there are no getters.

        :return: None.
        """
        notification = Notification.objects.create(receiver=self.ta)
        self.assertRaises(NotImplementedError, notification.get_ticket_url)
        self.assertRaises(NotImplementedError, notification.get_author)
        self.assertRaises(NotImplementedError, notification.get_title)
        self.assertRaises(NotImplementedError, notification.get_content)
        self.assertRaises(NotImplementedError, notification.get_inbox)
