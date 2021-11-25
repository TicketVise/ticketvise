from django.urls import reverse

from ticketvise.models.automation import Automation, AutomationCondition
from ticketvise.models.inbox import Inbox
from ticketvise.models.user import User, Role
from ticketvise.tests.test_ticket import TicketTestCase
from rest_framework.test import APIClient


class AutomationAPITestCase(TicketTestCase):

    def setUp(self):
        self.client = APIClient()

        self.inbox = Inbox.objects.create(name="TestInbox 1", code="TestCode1", color="#FF6600")
        self.inbox2 = Inbox.objects.create(name="TestInbox 2", code="TestCode2", color="#FF6600")

        self.assistant = User.objects.create(username="assistant", password="test67891",
                                             email="assistant@ticketvise.com")
        self.assistant.add_inbox(self.inbox)
        self.assistant.set_role_for_inbox(self.inbox, Role.AGENT)

        self.automation1 = Automation.objects.create(name="Test_automation 1", inbox=self.inbox,
                                                     action_func="assign_to",
                                                     action_value=self.assistant.id)
        self.automation2 = Automation.objects.create(name="Test_automation 2", inbox=self.inbox,
                                                     action_func="assign_to",
                                                     action_value=self.assistant.id)
        self.automation3 = Automation.objects.create(name="Test_automation 3", inbox=self.inbox2,
                                                     action_func="assign_to",
                                                     action_value=self.assistant.id)

    def test_get_automation_list(self):
        self.client.force_authenticate(self.assistant)
        response = self.client.get(reverse("automation_list", args=[self.inbox.id]))
        self.assertContains(response, self.automation1.name)
        self.assertContains(response, self.automation2.name)
        self.assertNotContains(response, self.automation3.name)

    def test_get_automation_list_conditions(self):
        self.client.force_authenticate(self.assistant)

        automation_condition1 = AutomationCondition.objects.create(
            automation=self.automation1,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="olifant")

        automation_condition2 = AutomationCondition.objects.create(
            automation=self.automation1,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="nijlpaard")

        automation_condition3 = AutomationCondition.objects.create(
            automation=self.automation1,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="giraffe")

        response = self.client.get(reverse("automation_list", args=[self.inbox.id]))
        self.assertContains(response, self.automation1.name)
        self.assertContains(response, automation_condition1.evaluation_value)
        self.assertContains(response, automation_condition2.evaluation_value)
        self.assertNotContains(response, automation_condition3.evaluation_value)
