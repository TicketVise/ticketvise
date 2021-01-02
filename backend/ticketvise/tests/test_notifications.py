"""
Test Notifications
-------------------------------
This file tests the notification functionality on the website.
"""

from django.test import TestCase, Client
from rest_framework.test import APIClient

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
        self.client = APIClient()
        self.inbox = Inbox.objects.create(code="ABC", name="how to code",
                                          scheduling_algorithm=SchedulingAlgorithm.FIXED)

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

        self.ticket = Ticket.objects.create(author=self.student, assignee=self.ta2,
                                            title="How to code?",
                                            inbox=self.inbox, content="wat is 1+1?")
        self.comment = Comment.objects.create(ticket=self.ticket, author=self.ta2, content="Hello World")

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
        self.client.force_authenticate(self.student)
        response = self.client.get("/api/notifications")
        self.assertEqual(response.status_code, 200)

    def test_notification_page_401(self):
        """
        Unauthorized users should be redirected to the login page. When logged in
        it should redirect to the notification page.

        :return: None.
        """
        response = self.client.get("/api/notifications")
        self.assertEqual(response.status_code, 401)

    def test_assigned_ticket(self):
        """
        If There is an assignee of a ticket, they must receive the notification.

        :return: None.
        """
        self.client.force_authenticate(self.ta)

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
        self.client.force_authenticate(self.ta)

        self.ticket.inbox.scheduling_algorithm = SchedulingAlgorithm.FIXED
        self.ticket.inbox.fixed_scheduling_assignee = None
        self.ticket.inbox.save()

        ticket = Ticket.objects.create(author=self.student, assignee=None, title="How to code v3?", inbox=self.inbox,
                                       content="wat is 3+1?")

        for user in self.ticket.inbox.get_assistants_and_coordinators():
            exists = NewTicketNotification.objects.filter(ticket=ticket, receiver=user).exists()
            self.assertTrue(exists)

    def test_mention_notification(self):
        """
        If a user is mentioned, it needs to receive a notification.

        :return: None.
        """
        self.client.force_authenticate(self.ta2)
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
        self.client.force_authenticate(self.student)

        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test", is_reply=False)

        self.assertFalse(CommentNotification.objects.filter(receiver=self.student).exists())

        Comment.objects.create(ticket=self.ticket, author=self.ta2, content="test", is_reply=True)

        self.assertTrue(CommentNotification.objects.filter(receiver=self.student).exists())

    def test_notification_settings(self):
        """
        If a user has disabled notifications, he should not receive any
        notifications in the notification panel.

        :return: None.
        """
        self.client.force_authenticate(self.ta)

        notifications = [
            (TicketAssignedNotification, "notification_assigned"),
            (TicketReminderNotification, "notification_ticket_reminder"),
            (NewTicketNotification, "notification_new_ticket"),
            (MentionNotification, "notification_mention"),
            (CommentNotification, "notification_comment"),
        ]

        for b in [True, False]:

            data = {}
            for _, key in notifications:
                for suffix in ["mail", "app"]:
                    data[key + "_" + suffix] = b

            response = self.client.put("/api/me/settings", data)
            self.assertEqual(response.status_code, 200)
            updated_user = User.objects.get(pk=self.ta.id)
            self.ticket.author = self.ta2

            for notification, key in notifications:
                Notification.objects.all().delete()

                for suffix in ["mail", "app"]:
                    self.assertEqual(getattr(updated_user, key + "_" + suffix), b)

                if hasattr(notification, "comment"):
                    notification(receiver=updated_user, comment=self.comment).save()
                elif hasattr(notification, "ticket"):
                    notification(receiver=updated_user, ticket=self.ticket).save()

                self.assertEqual(notification.objects.filter(receiver=updated_user).exists(), b)

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

    def test_getters_assigned_notifications(self):
        """
        Test all getters of the TicketAssignedNotification.

        :return: None.
        """
        ticket = Ticket.objects.create(author=self.student, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        assigned_notification = TicketAssignedNotification.objects.create(ticket=ticket, receiver=self.ta)
        self.assertEqual(assigned_notification.author, f"@{ticket.author.username}")
        self.assertEqual(assigned_notification.content, f"Ticket #{ticket.ticket_inbox_id} has been assigned to you")
        self.assertEqual(assigned_notification.inbox, ticket.inbox)

    def test_getters_new_ticket_notifications(self):
        """
        Test all getters of the NewTicketNotification.

        :return: None.
        """
        ticket = Ticket.objects.create(author=self.student, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        new_ticket_notification = NewTicketNotification.objects.create(ticket=ticket, receiver=self.ta)
        self.assertEqual(new_ticket_notification.author, f"@{ticket.author.username}")
        self.assertEqual(new_ticket_notification.content,
                         f"A new ticket has been created by {ticket.author.get_full_name()}")
        self.assertEqual(new_ticket_notification.inbox, ticket.inbox)

    def test_getters_reminder_notifications(self):
        """
        Test all getters of the TicketReminderNotification.

        :return: None.
        """
        ticket = Ticket.objects.create(author=self.student, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        reminder_notification = TicketReminderNotification.objects.create(ticket=ticket, receiver=self.ta)
        self.assertEqual(reminder_notification.author, f"@{ticket.author.username}")
        self.assertEqual(reminder_notification.content,
                         f"Ticket ${ticket.ticket_inbox_id} has been unanswered for {ticket.inbox.alert_coordinator_unanswered_days} days")
        self.assertEqual(reminder_notification.inbox, ticket.inbox)

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

    def test_duplicate_notification_on_mention(self):
        """
        Test to verify that the person being mentioned only receive a single mention notification, and not also a
        new comment notification. This test checks for issue #176.
        """
        Notification.objects.all().delete()

        ticket = Ticket.objects.create(author=self.student, assignee=self.ta,
                                       title="How to code?",
                                       inbox=self.inbox, content="wat is 1+1?")
        comment = Comment.objects.create(ticket=ticket, author=self.ta2, content="@admin", is_reply=False)
        self.assertTrue(MentionNotification.objects.filter(comment=comment, receiver=self.ta).exists())
        self.assertFalse(CommentNotification.objects.filter(comment=comment, receiver=self.ta).exists())

    def test_own_new_ticket_notification(self):
        ticket = Ticket.objects.create(author=self.ta, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        new_ticket_notification = NewTicketNotification.objects.create(ticket=ticket, receiver=self.ta)
        self.assertFalse(Notification.objects.filter(pk=new_ticket_notification.id).exists())

    def test_self_mention_notification(self):
        comment = Comment.objects.create(ticket=self.ticket, author=self.ta, content="@admin", is_reply=True)
        mention_notification = MentionNotification.objects.create(comment=comment, receiver=self.ta)

        self.assertFalse(Notification.objects.filter(id=mention_notification.id).exists())

    def test_own_ticket_reminder_notification(self):
        ticket = Ticket.objects.create(author=self.ta, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        reminder_notification = TicketReminderNotification.objects.create(ticket=ticket, receiver=self.ta)

        self.assertFalse(Notification.objects.filter(id=reminder_notification.id).exists())

    def test_email_comments(self):
        """
        Test if email_comments() returns the right comments
        """
        ticket = Ticket.objects.create(author=self.student, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        Comment.objects.create(ticket=ticket, author=self.student, content="wrong", is_reply=True)
        comments = [
            Comment.objects.create(ticket=ticket, author=self.student, content="first", is_reply=False),
            Comment.objects.create(ticket=ticket, author=self.student, content="second", is_reply=False),
            Comment.objects.create(ticket=ticket, author=self.student, content="third", is_reply=False),
        ]
        comment_notification = CommentNotification.objects.create(comment=comments[1], receiver=self.ta)
        self.assertEqual(list(comment_notification.get_email_comments()), comments)

    def test_email_replies(self):
        """
        Test if email_comments() returns the right replies
        """
        ticket = Ticket.objects.create(author=self.student, assignee=None, title="TestTicket", inbox=self.inbox,
                                       content="TestTicket")
        Comment.objects.create(ticket=ticket, author=self.student, content="wrong", is_reply=False),
        replies = [
            Comment.objects.create(ticket=ticket, author=self.student, content="first", is_reply=True),
            Comment.objects.create(ticket=ticket, author=self.student, content="second", is_reply=True),
            Comment.objects.create(ticket=ticket, author=self.student, content="third", is_reply=True),
        ]
        comment_notification = CommentNotification.objects.create(comment=replies[1], receiver=self.ta)
        self.assertEqual(list(comment_notification.get_email_comments()), replies)

    def test_get_notifications_200(self):
        self.client.force_authenticate(self.student)
        response = self.client.get("/api/notifications")
        self.assertEqual(response.status_code, 200)

    def test_get_notifications_unauthorized(self):
        response = self.client.get("/api/notifications")
        self.assertEqual(response.status_code, 401)

    def test_get_notifications_count(self):
        self.client.force_authenticate(self.ta)
        Notification.objects.all().delete()

        MentionNotification.objects.create(receiver=self.ta, is_read=True, comment=self.comment)
        CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=self.comment)
        TicketAssignedNotification.objects.create(receiver=self.ta, is_read=True, ticket=self.ticket)
        NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)
        TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)

        response = self.client.get("/api/notifications/unread")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '3')

    def test_get_notifications_all(self):
        self.client.force_authenticate(self.ta)

        data = {
            "is_read": ""
        }

        Notification.objects.all().delete()

        MentionNotification.objects.create(receiver=self.ta, is_read=True, comment=self.comment),
        CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=self.comment),
        TicketAssignedNotification.objects.create(receiver=self.ta, is_read=True, ticket=self.ticket),
        NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
        TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)

        response = self.client.get("/api/notifications", data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"count":5')

    def test_get_notifications_read(self):
        self.client.force_authenticate(self.ta)

        data = {
            "is_read": "True"
        }

        Notification.objects.all().delete()

        MentionNotification.objects.create(receiver=self.ta, is_read=True, comment=self.comment),
        CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=self.comment),
        TicketAssignedNotification.objects.create(receiver=self.ta, is_read=True, ticket=self.ticket),
        NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
        TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)

        response = self.client.get("/api/notifications", data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"count":2')

    def test_get_notifications_unread(self):
        self.client.force_authenticate(self.ta)

        data = {
            "is_read": "False"
        }

        Notification.objects.all().delete()

        MentionNotification.objects.create(receiver=self.ta, is_read=True, comment=self.comment),
        CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=self.comment),
        TicketAssignedNotification.objects.create(receiver=self.ta, is_read=True, ticket=self.ticket),
        NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
        TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)

        response = self.client.get("/api/notifications", data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"count":3')

    def test_notifications_read_all(self):
        self.client.force_authenticate(self.ta)

        comment = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)

        notifications = [
            MentionNotification.objects.create(receiver=self.ta, is_read=False, comment=comment),
            CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=comment),
            TicketAssignedNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)
        ]

        for notification in notifications:
            self.assertFalse(Notification.objects.get(pk=notification.id).is_read)

        response = self.client.put("/api/notifications/read/all")
        self.assertEqual(response.status_code, 200)

        for notification in notifications:
            self.assertTrue(Notification.objects.get(pk=notification.id).is_read)

    def test_notifications_read_on_ticket_view(self):
        self.client.force_authenticate(self.ta)

        comment1 = Comment.objects.create(ticket=self.ticket, author=self.student, content="@admin", is_reply=True)

        notifications1 = [
            MentionNotification.objects.create(receiver=self.ta, is_read=False, comment=comment1),
            CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=comment1),
            TicketAssignedNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket),
            TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket)
        ]

        comment2 = Comment.objects.create(ticket=self.ticket_2, author=self.student, content="@admin", is_reply=True)
        notifications2 = [
            MentionNotification.objects.create(receiver=self.ta, is_read=False, comment=comment2),
            CommentNotification.objects.create(receiver=self.ta, is_read=False, comment=comment2),
            TicketAssignedNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket_2),
            NewTicketNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket_2),
            TicketReminderNotification.objects.create(receiver=self.ta, is_read=False, ticket=self.ticket_2)
        ]

        for notification in notifications1:
            self.assertFalse(Notification.objects.get(pk=notification.id).is_read)

        for notification in notifications2:
            self.assertFalse(Notification.objects.get(pk=notification.id).is_read)

        response = self.client.get(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}")
        self.assertEqual(response.status_code, 200)

        for notification in notifications1:
            self.assertTrue(Notification.objects.get(pk=notification.id).is_read)

        for notification in notifications2:
            self.assertFalse(Notification.objects.get(pk=notification.id).is_read)

    def test_notifications_flip_read(self):
        self.client.force_authenticate(self.ta)

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

    def test_set_assignee(self):
        self.client.force_authenticate(self.ta2)

        self.ticket.assignee = None
        self.ticket.save()

        Notification.objects.all().delete()

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.ta.id})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.assignee, self.ta)

        exists = TicketAssignedNotification.objects.filter(ticket=self.ticket, receiver=self.ta).exists()
        self.assertTrue(exists)

    def test_set_assignee_self(self):
        self.client.force_authenticate(self.ta)

        self.ticket.assignee = None
        self.ticket.save()

        Notification.objects.all().delete()

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/tickets/{self.ticket.ticket_inbox_id}/assignee",
                                   data={"assignee": self.ta.id})
        self.assertEqual(response.status_code, 200)

        ticket = Ticket.objects.get(pk=self.ticket.id)
        self.assertEqual(ticket.assignee, self.ta)

        exists = TicketAssignedNotification.objects.filter(ticket=self.ticket, receiver=self.ta).exists()
        self.assertFalse(exists)
