from django.urls import reverse

from ticketvise.models.label import Label
from ticketvise.tests.inbox.utils import InboxTestCase


class LabelsTest(InboxTestCase):

    def test_delete_label_as_coordinator(self):
        """
        Test to verify a coordinator is able to delete a label.
        """
        self.client.force_login(self.coordinator)

        response = self.client.delete(reverse("api_inbox_label", args=(self.label.inbox.id, self.label.id)),
                                      follow=True)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Label.objects.filter(pk=self.label.id).exists())

    def test_delete_label_as_assistant(self):
        """
        Test to verify a assistant is unable to delete a label.
        """

        self.client.force_login(self.assistant)

        response = self.client.delete(reverse("api_inbox_label", args=(self.label.inbox.id, self.label.id)),
                                      follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.id).exists())

    def test_delete_label_as_student(self):
        """
        Test to verify a student is unable to delete a label.
        """
        self.client.force_login(self.student)

        response = self.client.delete(reverse("api_inbox_label", args=(self.label.inbox.id, self.label.id)),
                                      follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.id).exists())

    def test_delete_label_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another inbox is unable to delete a label.
        """
        self.client.force_login(self.coordinator_2)

        response = self.client.delete(reverse("api_inbox_label", args=(self.label.inbox.id, self.label.id)),
                                      follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.id).exists())

    def test_add_label_as_coordinator(self):
        """
        Test to verify a coordinator is able to create a label.
        """
        self.client.force_login(self.coordinator)

        data = {
            "name": "test_name",
            "color": "#ff3333",
            "is_visible_to_guest": "on",
            "is_active": "on"
        }

        response = self.client.post(reverse("api_new_inbox_label", args=(self.inbox.id,)), data, follow=True)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Label.objects.filter(name=data["name"]).exists())

    def test_add_label_as_assistant(self):
        """
        Test to verify a assistant is unable to create a label.
        """
        self.client.force_login(self.assistant)

        data = {
            "name": "test_name",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.post(reverse("api_new_inbox_label", args=(self.inbox.id,)), data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Label.objects.filter(name=data["name"]).exists())

    def test_add_label_as_student(self):
        """
        Test to verify a student is unable to create a label.
        """
        self.client.force_login(self.assistant)

        data = {
            "name": "test_name",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.post(reverse("api_new_inbox_label", args=(self.inbox.id,)), data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Label.objects.filter(name=data["name"]).exists())

    def test_add_invalid_label(self):
        """
        Test to verify an invalid submission of invalid label data shouldn't be processed.
        """
        self.client.force_login(self.coordinator)

        data = {
            "name": "",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.post(reverse("api_new_inbox_label", args=(self.inbox.id,)), data, follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Label.objects.filter(name=data["name"]).exists())

    def test_edit_label_as_coordinator(self):
        """
        Test to verify a coordinator is able to edit a label.
        """
        self.client.force_login(self.coordinator)

        data = {
            "name": "345345",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.put(reverse("api_inbox_label", args=(self.inbox.id, self.label.id)), data, follow=True,
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.get(pk=self.label.id).name, data["name"])

    def test_edit_label_as_invalid_coordinator(self):
        """
        Test to verify a coordinator form another inbox is unable to edit a label.
        """
        self.client.force_login(self.coordinator_2)

        data = {
            "name": "345345",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.put(reverse("api_inbox_label", args=(self.inbox.id, self.label.id)), data,
                                   follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Label.objects.get(pk=self.label.id).name, data["name"])

    def test_edit_label_as_assistant(self):
        """
        Test to verify a assistant is unable to edit a label.
        """
        self.client.force_login(self.assistant)

        data = {
            "name": "345345",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.put(reverse("api_inbox_label", args=(self.inbox.id, self.label.id)), data,
                                   follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Label.objects.get(pk=self.label.id).name, data["name"])

    def test_edit_label_as_student(self):
        """
        Test to verify a student is unable to edit a label.
        """
        self.client.force_login(self.student)

        data = {
            "name": "345345",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.put(reverse("api_inbox_label", args=(self.inbox.id, self.label.id)), data,
                                   follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Label.objects.get(pk=self.label.id).name, data["name"])

    def test_inbox_invisible_label_student(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.invisible_label.name)

    def test_inbox_invisible_label_agent(self):
        self.client.force_login(self.assistant)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invisible_label.name)

    def test_inbox_invisible_label_manager(self):
        self.client.force_login(self.coordinator)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.invisible_label.name)

    def test_inbox_inactive_label_student(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.disabled_label.name)

    def test_inbox_inactive_label_agent(self):
        self.client.force_login(self.assistant)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.disabled_label.name)

    def test_inbox_inactive_label_manager(self):
        self.client.force_login(self.coordinator)

        response = self.client.get(reverse("api_all_inbox_labels", args=(self.inbox.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.disabled_label.name)
