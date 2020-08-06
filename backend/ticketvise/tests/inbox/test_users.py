from django.urls import reverse

from ticketvise.models.user import UserInbox
from ticketvise.tests.inbox.utils import InboxTestCase


class UsersTest(InboxTestCase):
    data = {
        "role": "Coordinator",
    }

    def edit_user(self):
        return self.client.post(reverse("inbox_user", args=(self.inbox.id, self.student.id)), self.data, follow=True)

    def test_edit_user_as_coordinator(self):
        """
        Test to verify a coordinator is able to edit a user.
        """
        self.client.force_login(self.coordinator)
        self.assertEqual(self.edit_user().status_code, 200)
        self.assertEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                         self.data["role"])

    def test_edit_user_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another inbox is unable to edit a user.
        """
        self.client.force_login(self.coordinator_2)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                            self.data["role"])

    def test_edit_user_as_assistant(self):
        """
        Test to verify a assistant is unable to edit a user.
        """
        self.client.force_login(self.assistant)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                            self.data["role"])

    def test_edit_user_as_student(self):
        """
        Test to verify a student is unable to edit a user.
        """
        self.client.force_login(self.student)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                            self.data["role"])
