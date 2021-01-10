from ticketvise.models.inbox import Inbox, SchedulingAlgorithm
from ticketvise.tests.inbox.utils import InboxTestCase


class SettingsTestCase(InboxTestCase):
    def test_edit_inbox_as_coordinator(self):
        """
        Test to verify a coordinator is able to edit a inbox.
        """
        self.client.force_authenticate(self.coordinator)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "fixed"
        }

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/settings", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inbox.objects.get(pk=self.inbox.id).name, data["name"])

    def test_edit_inbox_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another inbox is unable to edit a inbox.
        """
        self.client.force_authenticate(self.coordinator_2)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "fixed"
        }

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/settings", data)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Inbox.objects.get(pk=self.inbox.id).name, data["name"])

    def test_edit_inbox_as_assistant(self):
        """
        Test to verify a assistant is unable to edit a inbox.
        """
        self.client.force_authenticate(self.assistant)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "fixed"
        }

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/settings", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Inbox.objects.get(pk=self.inbox.id).name, data["name"])

    def test_edit_inbox_as_student(self):
        """
        Test to verify a student is unable to edit a inbox.
        """
        self.client.force_authenticate(self.student)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "fixed"
        }

        response = self.client.put(f"/api/inboxes/{self.inbox.id}/settings", data)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Inbox.objects.get(pk=self.inbox.id).name, data["name"])

    def test_get_inbox_attributes(self):
        self.client.force_authenticate(self.coordinator)
        response = self.client.get(f"/api/inboxes/{self.inbox.id}/settings")
        self.assertContains(response, self.inbox.name)
        self.assertContains(response, self.assistant)
        self.assertContains(response, "Workgroup")

