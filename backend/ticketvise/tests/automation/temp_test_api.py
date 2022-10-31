from django.urls import reverse

from ticketvise.models.automation import Automation, AutomationCondition
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Ticket
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
            automation=self.automation3,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="giraffe")

        response = self.client.get(reverse("automation_list", args=[self.inbox.id]))
        self.assertContains(response, self.automation1.name)
        self.assertContains(response, automation_condition1.evaluation_value)
        self.assertContains(response, automation_condition2.evaluation_value)
        self.assertNotContains(response, automation_condition3.evaluation_value)

    def test_create_automation(self):
        self.client.force_authenticate(self.assistant)

        data = {
            "name": "Test automation",
            "action_func": "assign_to",
            "action_value": self.assistant.id
        }

        response = self.client.post(reverse("create_automation", args=[self.inbox.id]), data)
        self.assertEqual(response.status_code, 201)
        Automation.objects.get(inbox=self.inbox, name=data["name"])

    def test_create_automation_condition(self):
        self.client.force_authenticate(self.assistant)

        data = {
            "field_name": "title",
            "evaluation_func": "contains",
            "evaluation_value": "leeuw"
        }

        response = self.client.post(reverse("create_automation_condition", args=[self.inbox.id, self.automation1.id]),
                                    data)
        self.assertEqual(response.status_code, 201)
        AutomationCondition.objects.get(automation=self.automation1, field_name="title", evaluation_value="leeuw")

    def test_get_automation_condition(self):
        self.client.force_authenticate(self.assistant)
        condition = AutomationCondition.objects.create(
            automation=self.automation1,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hond"
        )

        response = self.client.get(
            reverse("update_retrieve_automation_condition", args=[self.inbox.id, self.automation1.id, condition.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "hond")

    def test_update_automation_condition(self):
        self.client.force_authenticate(self.assistant)
        condition = AutomationCondition.objects.create(
            automation=self.automation1,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hond"
        )

        data = {
            "field_name": "title",
            "evaluation_func": "eq",
            "evaluation_value": "kat"
        }

        response = self.client.put(
            reverse("update_retrieve_automation_condition", args=[self.inbox.id, self.automation1.id, condition.id]),
            data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data["evaluation_value"])

        condition = AutomationCondition.objects.get(pk=condition.id)
        self.assertEqual(condition.evaluation_value, data["evaluation_value"])

    def test_get_automation(self):
        self.client.force_authenticate(self.assistant)
        automation = Automation.objects.create(name="Test_automation temp 1",
                                               inbox=self.inbox,
                                               action_func="assign_to",
                                               action_value=self.assistant.id)

        response = self.client.get(reverse("update_retrieve_automation", args=[self.inbox.id, automation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test_automation temp 1")

    def test_update_automation(self):
        self.client.force_authenticate(self.assistant)
        automation = Automation.objects.create(name="Test_automation temp 1",
                                               inbox=self.inbox,
                                               action_func="assign_to",
                                               action_value=self.assistant.id)

        data = {
            "name": "Een nieuwe naam",
            "action_func": "assign_to",
            "action_value": self.assistant.id
        }

        response = self.client.put(reverse("update_retrieve_automation", args=[self.inbox.id, automation.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, data["name"])

        automation = Automation.objects.get(pk=automation.id)
        self.assertEqual(automation.name, data["name"])
