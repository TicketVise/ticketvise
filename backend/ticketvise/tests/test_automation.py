from django.core.exceptions import ValidationError, FieldDoesNotExist

from ticketvise.models.automation import Automation, AutomationCondition
from ticketvise.models.inbox import Inbox
from ticketvise.models.ticket import Status, Ticket
from ticketvise.models.user import Role, User
from ticketvise.models.label import Label
from ticketvise.tests.test_ticket import TicketTestCase


class AutomationTestCase(TicketTestCase):

    def setUp(self):
        self.inbox = Inbox.objects.create(name="TestInbox", code="TestCode", color="#FF6600")

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

        self.automation = Automation.objects.create(name="Test1", inbox=self.inbox, action_func="assign_to",
                                                    action_value=self.assistant.id)
        self.ticket = Ticket.objects.create(author=self.student,
                                            assignee=self.assistant, title="hetwerkt", content="lol",
                                            inbox=self.inbox, status=Status.ASSIGNED)

    def test_equals_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hetwerkt")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_equals_foreign_key_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="author",
            evaluation_func="eq",
            evaluation_value=str(self.ticket.author.id))
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_equals_datetime_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="is_public",
            evaluation_func="isset",
            evaluation_value="True")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_equals_boolean_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="is_anonymous",
            evaluation_func="eq",
            evaluation_value="False")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_equals_many_to_many_empty_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="labels",
            evaluation_func="eq",
            evaluation_value='1')
        result = automation_condition(self.ticket)
        self.assertFalse(result)
        self.assertEqual(self.ticket.labels.count(), 0)

    def test_equals_many_to_many_valid(self):
        ticket = self.ticket
        label = Label.objects.create(inbox=self.ticket.inbox, name="first label")
        ticket.add_label(label)
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="labels",
            evaluation_func="eq",
            evaluation_value=str(label.id))
        result = automation_condition(ticket)
        self.assertTrue(result)
        self.assertNotEqual(ticket.labels.count(), 0)

    def test_equals_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hetwerktniet")
        result = automation_condition(self.ticket)
        self.assertFalse(result)

    def test_gt_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="gt",
            evaluation_value="2000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_gt_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="gt",
            evaluation_value="3000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertFalse(result)

        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="gt",
            evaluation_value=self.ticket.date_created.isoformat())
        result = automation_condition(self.ticket)
        self.assertFalse(result)

    def test_ge_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="ge",
            evaluation_value="2000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="ge",
            evaluation_value=self.ticket.date_created.isoformat())
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_ge_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="ge",
            evaluation_value="3000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertFalse(result)

    def test_lt_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="lt",
            evaluation_value="3000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_lt_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="lt",
            evaluation_value="2000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertFalse(result)

        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="lt",
            evaluation_value=self.ticket.date_created.isoformat())
        result = automation_condition(self.ticket)
        self.assertFalse(result)

    def test_le_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="le",
            evaluation_value="3000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="le",
            evaluation_value=self.ticket.date_created.isoformat())
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_le_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="date_created",
            evaluation_func="le",
            evaluation_value="2000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertFalse(result)

    def test_contains_charfield_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="title",
            evaluation_func="contains",
            evaluation_value="werkt")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_contains_charfield_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="title",
            evaluation_func="contains",
            evaluation_value="olifant")
        result = automation_condition(self.ticket)
        self.assertFalse(result)
        self.assertFalse(result)

    def test_contains_many_to_many_valid(self):
        ticket = self.ticket
        label1 = Label.objects.create(inbox=self.ticket.inbox, name="first label")
        label2 = Label.objects.create(inbox=self.ticket.inbox, name="second label")
        ticket.add_label(label1)
        ticket.add_label(label2)
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="labels",
            evaluation_func="contains",
            evaluation_value=str(label1.id))
        result = automation_condition(ticket)
        self.assertTrue(result)

    def test_contains_many_to_many_invalid(self):
        ticket = self.ticket
        label1 = Label.objects.create(inbox=self.ticket.inbox, name="first label")
        label2 = Label.objects.create(inbox=self.ticket.inbox, name="second label")
        ticket.add_label(label1)
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="labels",
            evaluation_func="contains",
            evaluation_value=str(label2.id))
        result = automation_condition(ticket)
        self.assertFalse(result)

    def test_assign_to_valid(self):
        automation = Automation.objects.create(name="Test1", inbox=self.inbox, action_func="assign_to",
                                               action_value=self.assistant2.id)
        AutomationCondition.objects.create(
            automation=automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hetwerkt")

        self.assertEqual(self.ticket.assignee, self.assistant)
        automation.execute(self.ticket)
        self.assertEqual(self.ticket.assignee, self.assistant2)

    def test_add_label_valid(self):
        ticket = self.ticket
        label = Label.objects.create(inbox=self.ticket.inbox, name="first label")

        automation = Automation.objects.create(name="Test1", inbox=self.inbox, action_func="add_label",
                                               action_value=label.id)
        AutomationCondition.objects.create(
            automation=automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hetwerkt")

        self.assertEqual(ticket.labels.count(), 0)
        automation.execute(ticket)
        self.assertEqual(ticket.labels.count(), 1)

    def test_multiple_conditions_valid(self):
        ticket = self.ticket
        label = Label.objects.create(inbox=self.ticket.inbox, name="first label")

        automation = Automation.objects.create(name="Test1", inbox=self.inbox, action_func="add_label",
                                               action_value=label.id)
        AutomationCondition.objects.create(
            automation=automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="hetwerkt")
        AutomationCondition.objects.create(
            automation=automation,
            field_name="content",
            evaluation_func="contains",
            evaluation_value="ol")
        AutomationCondition.objects.create(
            automation=automation,
            field_name="assignee",
            evaluation_func="eq",
            evaluation_value=self.assistant.id)

        self.assertEqual(ticket.labels.count(), 0)
        automation.execute(ticket)
        self.assertEqual(ticket.labels.count(), 1)

    def test_multiple_conditions_invalid(self):
        ticket = self.ticket
        label = Label.objects.create(inbox=self.ticket.inbox, name="first label")

        automation = Automation.objects.create(name="Test1", inbox=self.inbox, action_func="add_label",
                                               action_value=label.id)
        AutomationCondition.objects.create(
            automation=automation,
            field_name="content",
            evaluation_func="contains",
            evaluation_value="ol")
        AutomationCondition.objects.create(
            automation=automation,
            field_name="assignee",
            evaluation_func="eq",
            evaluation_value=self.assistant.id)
        AutomationCondition.objects.create(
            automation=automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="staaternietin")

        self.assertEqual(ticket.labels.count(), 0)
        automation.execute(ticket)
        self.assertEqual(ticket.labels.count(), 0)

    def test_invalid_condition_field_name(self):
        with self.assertRaises(FieldDoesNotExist):
            AutomationCondition.objects.create(
                automation=self.automation,
                field_name="foo",
                evaluation_func="eq",
                evaluation_value="ol")

    def test_negate(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            field_name="title",
            evaluation_func="eq",
            evaluation_value="foo",
            negation=True)
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_invalid_condition_function(self):
        with self.assertRaises(ValidationError):
            AutomationCondition.objects.create(
                automation=self.automation,
                field_name="content",
                evaluation_func="wrong",
                evaluation_value="ol")

    def test_invalid_value_type(self):
        with self.assertRaises(ValidationError):
            AutomationCondition.objects.create(
                automation=self.automation,
                field_name="labels",
                evaluation_func="eq",
                evaluation_value="label")

    def test_invalid_datetime_value(self):
        with self.assertRaises(ValidationError):
            AutomationCondition.objects.create(
                automation=self.automation,
                field_name="date_created",
                evaluation_func="gt",
                evaluation_value="label")
