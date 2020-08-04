from django.urls import reverse

from ticketvise.models.inbox import Course
from ticketvise.tests.course.utils import CourseTestCase


class SettingsTestCase(CourseTestCase):
    def test_edit_course_as_coordinator(self):
        """
        Test to verify a coordinator is able to edit a course.
        """
        self.client.force_login(self.coordinator)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "image": "",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "manual"
        }

        response = self.client.post(reverse("course_settings", args=(self.course.id,)), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.objects.get(pk=self.course.id).name, data["name"])

    def test_edit_course_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another course is unable to edit a course.
        """
        self.client.force_login(self.coordinator_2)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "image": "",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "manual"
        }

        response = self.client.post(reverse("course_settings", args=(self.course.id,)), data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Course.objects.get(pk=self.course.id).name, data["name"])

    def test_edit_course_as_assistant(self):
        """
        Test to verify a assistant is unable to edit a course.
        """
        self.client.force_login(self.assistant)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "image": "",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "manual"
        }

        response = self.client.post(reverse("course_settings", args=(self.course.id,)), data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Course.objects.get(pk=self.course.id).name, data["name"])

    def test_edit_course_as_student(self):
        """
        Test to verify a student is unable to edit a course.
        """
        self.client.force_login(self.student)

        data = {
            "name": "Andere naam",
            "code": "5062STRE6Y22",
            "color": "#1c7225",
            "image": "",
            "close_answered_weeks": "1",
            "alert_coordinator_unanswered_days": "2",
            "scheduling_algorithm": "manual"
        }

        response = self.client.post(reverse("course_settings", args=(self.course.id,)), data, follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Course.objects.get(pk=self.course.id).name, data["name"])
