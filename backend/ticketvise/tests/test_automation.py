from ticketvise.tests.test_ticket import TicketTestCase
from ticketvise.models.inbox import Inbox
from ticketvise.models.automation import Automation, AutomationCondition
from ticketvise.models.ticket import Status, Ticket
from ticketvise.models.user import Role, User

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

        self.automation = Automation.objects.create(name="Test1", inbox=self.inbox)
        self.ticket = Ticket.objects.create(author=self.student,
            assignee=self.assistant, title="hetwerkt", content="lol",
            inbox=self.inbox, status=Status.ASSIGNED)

    def test_equals_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            index=0,
            field_name="title",
            evaluation_func="equals",
            evaluation_value="hetwerkt")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_equals_foreign_key_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            index=0,
            field_name="author",
            evaluation_func="equals",
            evaluation_value=str(self.ticket.author.username))
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    def test_equals_invalid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            index=0,
            field_name="title",
            evaluation_func="equals",
            evaluation_value="hetwerktniet")
        result = automation_condition(self.ticket)
        self.assertFalse(result)

    def test_gt_valid(self):
        automation_condition = AutomationCondition.objects.create(
            automation=self.automation,
            index=0,
            field_name="date_created",
            evaluation_func="gt",
            evaluation_value="2000-08-27T09:32:21+02:00")
        result = automation_condition(self.ticket)
        self.assertTrue(result)

    # def test_gt_invalid(self):
    #     automation_condition = AutomationCondition.objects.create(
    #         automation=self.automation,
    #         index=0,
    #         field_name="title",
    #         evaluation_func="equals",
    #         evaluation_value="hetwerktniet")
    #     result = automation_condition(self.ticket)
    #     self.assertFalse(result)