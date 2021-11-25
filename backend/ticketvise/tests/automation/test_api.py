from django.urls import reverse

from ticketvise.models.automation import Automation
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket, Status
from ticketvise.models.user import User, Role
from ticketvise.tests.test_ticket import TicketTestCase


class AutomationAPITestCase(TicketTestCase):

    def setUp(self):
        self.inbox = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")
        self.inbox2 = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")

        self.student = User.objects.create(username="student", password="test12345", email="student@ticketvise.com")
        self.student.add_inbox(self.inbox)
        self.student.set_role_for_inbox(self.inbox, Role.GUEST)

        self.assistant = User.objects.create(username="assistant", password="test67891",
                                             email="assistant@ticketvise.com")
        self.assistant.add_inbox(self.inbox)
        self.assistant.set_role_for_inbox(self.inbox, Role.AGENT)

        self.assistant2 = User.objects.create(username="assistant2", password="test67891",
                                              email="assistant2@ticketvise.com")
        self.assistant2.add_inbox(self.inbox)
        self.assistant2.set_role_for_inbox(self.inbox, Role.AGENT)

        self.automation1 = Automation.objects.create(name="Test_automation 1", inbox=self.inbox, action_func="assign_to",
                                                    action_value=self.assistant.id)
        self.automation2 = Automation.objects.create(name="Test_automation 2", inbox=self.inbox, action_func="assign_to",
                                                    action_value=self.assistant.id)
        self.automation3 = Automation.objects.create(name="Test_automation 3", inbox=self.inbox2, action_func="assign_to",
                                                    action_value=self.assistant.id)

        self.ticket = Ticket.objects.create(author=self.student,
                                            assignee=self.assistant, title="hetwerkt", content="lol",
                                            inbox=self.inbox, status=Status.ASSIGNED)

    def test_get_automation_list(self):
        self.client.force_authenticate(self.assistant)
        response = self.client.get(reverse("automation_list", args=[self.inbox]))
        self.assertContains(response, self.automation1.name)
        self.assertContains(response, self.automation2.name)
        self.assertNotContains(response, self.automation3.name)
