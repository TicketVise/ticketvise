from django.urls import reverse

from ticketvise.models.user import UserInbox, Role
from ticketvise.tests.inbox.utils import InboxTestCase


class UsersTest(InboxTestCase):
    data = {
        "role": Role.MANAGER,
    }

    def edit_user(self):
        return self.client.put("/api/inboxes/{}/users/{}".format(self.inbox.id, self.student.id), self.data)

    def test_edit_user_as_coordinator(self):
        """
        Test to verify a coordinator is able to edit a user.
        """
        self.client.force_authenticate(self.coordinator)
        self.assertEqual(self.edit_user().status_code, 200)
        self.assertEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                         self.data["role"])

    def test_edit_user_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another inbox is unable to edit a user.
        """
        self.client.force_authenticate(self.coordinator_2)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                            self.data["role"])

    def test_edit_user_as_assistant(self):
        """
        Test to verify a assistant is unable to edit a user.
        """
        self.client.force_authenticate(self.assistant)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                            self.data["role"])

    def test_edit_user_as_student(self):
        """
        Test to verify a student is unable to edit a user.
        """
        self.client.force_authenticate(self.student)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserInbox.objects.get(user_id=self.student.id, inbox__id=self.inbox.id).role,
                            self.data["role"])

    def test_users(self):
        self.client.force_authenticate(self.coordinator)
        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users")
        self.assertContains(response, self.student.username)
        self.assertContains(response, self.student3.username)
        self.assertNotContains(response, self.student2.username)

    def test_users_search(self):
        self.client.force_authenticate(self.coordinator)

        self.client.force_authenticate(self.coordinator)
        response = self.client.get(f"/api/inboxes/{self.inbox.id}/users", {"q": "aa"})
        self.assertContains(response, self.student3.username)
        self.assertNotContains(response, self.student2.username)
        self.assertNotContains(response, self.student.username)