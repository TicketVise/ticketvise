from django.urls import reverse

from ticketvise.models.label import Label
from ticketvise.tests.course.utils import CourseTestCase


class LabelsTest(CourseTestCase):

    def test_delete_label_as_coordinator(self):
        """
        Test to verify a coordinator is able to delete a label.
        """
        self.client.force_login(self.coordinator)

        response = self.client.post(reverse("delete_course_label", args=(self.label.course.id, self.label.id)),
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Label.objects.filter(pk=self.label.id).exists())

    def test_delete_label_as_assistant(self):
        """
        Test to verify a assistant is unable to delete a label.
        """
        self.client.force_login(self.assistant)

        response = self.client.post(reverse("delete_course_label", args=(self.label.course.id, self.label.id)),
                                    follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.id).exists())

    def test_delete_label_as_student(self):
        """
        Test to verify a student is unable to delete a label.
        """
        self.client.force_login(self.student)

        response = self.client.post(reverse("delete_course_label", args=(self.label.course.id, self.label.id)),
                                    follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Label.objects.filter(pk=self.label.id).exists())

    def test_delete_label_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another course is unable to delete a label.
        """
        self.client.force_login(self.coordinator_2)

        response = self.client.post(reverse("delete_course_label", args=(self.label.course.id, self.label.id)),
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
            "is_form_label": "on",
            "is_active": "on"
        }

        response = self.client.post(reverse("create_course_label", args=(self.course.id,)), data, follow=True)
        self.assertEqual(response.status_code, 200)
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

        response = self.client.post(reverse("create_course_label", args=(self.course.id,)), data, follow=True)
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

        response = self.client.post(reverse("create_course_label", args=(self.course.id,)), data, follow=True)
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

        self.client.post(reverse("create_course_label", args=(self.course.id,)), data, follow=True)
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

        response = self.client.post(reverse("edit_course_label", args=(self.course.id, self.label.id)), data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.get(pk=self.label.id).name, data["name"])

    def test_edit_label_as_invalid_coordinator(self):
        """
        Test to verify a coordinator form another course is unable to edit a label.
        """
        self.client.force_login(self.coordinator_2)

        data = {
            "name": "345345",
            "color": "#ff3333",
            "student-available": "yes",
            "active": "yes"
        }

        response = self.client.post(reverse("edit_course_label", args=(self.course.id, self.label.id)), data,
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

        response = self.client.post(reverse("edit_course_label", args=(self.course.id, self.label.id)), data,
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

        response = self.client.post(reverse("edit_course_label", args=(self.course.id, self.label.id)), data,
                                    follow=True)
        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(Label.objects.get(pk=self.label.id).name, data["name"])
