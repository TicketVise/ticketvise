from django.test import TestCase, Client

from ticketvise.models.label import Label
from ticketvise.models.user import User, Role
from ticketvise.tests.utils import create_label, create_inbox


class InboxTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the inbox related tests.
        """
        self.client = Client()
        self.student = User.objects.create_user(
            username="student", email="root@ticketvise.com", password="test12345", is_staff=False
        )
        self.student.set_password("test12345")
        self.student.save()

        self.student2 = User.objects.create_user(username="dfg34gf", email="dfgdf@ticketvise.com")
        self.student3 = User.objects.create_user(username="aaaaa", email="aaaaa@ticketvise.com")

        self.assistant = User.objects.create_user(
            username="assistant", email="assitant@ticketvise.com", password="test12345", is_staff=False
        )
        self.assistant.set_password("test12345")
        self.assistant.save()

        self.coordinator = User.objects.create_user(
            username="coordinator", email="coordinator@ticketvise.com", password="test12345", is_staff=False
        )
        self.coordinator.set_password("test12345")
        self.coordinator.save()

        self.coordinator_2 = User.objects.create_user(
            username="coordinator2", email="coordinator2@ticketvise.com", password="test12345", is_staff=False)

        self.inbox = create_inbox("inbox_1_name", "inbox_1_code")
        self.inbox_2 = create_inbox("inbox_2_name", "inbox_2_code")

        self.student.add_inbox(self.inbox, Role.GUEST)
        self.student.add_inbox(self.inbox_2, Role.GUEST)
        self.student2.add_inbox(self.inbox_2, Role.GUEST)
        self.student3.add_inbox(self.inbox, Role.GUEST)
        self.assistant.add_inbox(self.inbox, Role.AGENT)
        self.coordinator.add_inbox(self.inbox, Role.MANAGER)
        self.coordinator_2.add_inbox(self.inbox_2, Role.MANAGER)
        self.label = create_label(inbox=self.inbox)
        self.label_2 = create_label(inbox=self.inbox_2)
        self.invisible_label = Label.objects.create(name="invisible", inbox=self.inbox, is_visible_to_guest=False)
        self.disabled_label = Label.objects.create(name="disabled", inbox=self.inbox, is_active=False)

        self.template_names = [
            ("inbox_user", (self.inbox.id, self.student.id)),
            ("inbox_users", (self.inbox.id,)),
            ("inbox_labels", (self.inbox.id,)),
            ("inbox_settings", (self.inbox.id,)),
            ("create_inbox_label", (self.inbox.id,)),
            ("inbox_statistics", (self.inbox.id,)),
            ("edit_inbox_label", (self.inbox.id, self.label.id)),
            ("delete_inbox_label", (self.inbox.id, self.label.id)),
            ("inbox_user_delete", (self.inbox.id, self.student.id)),
        ]
