from django.urls import reverse

from ticketvise.models.user import UserCourseRelationship
from ticketvise.tests.course.utils import CourseTestCase


class UsersTest(CourseTestCase):
    data = {
        "role": "Coordinator",
    }

    def edit_user(self):
        return self.client.post(reverse("course_user", args=(self.course.id, self.student.id)), self.data, follow=True)

    def test_edit_user_as_coordinator(self):
        """
        Test to verify a coordinator is able to edit a user.
        """
        self.client.force_login(self.coordinator)
        self.assertEqual(self.edit_user().status_code, 200)
        self.assertEqual(UserCourseRelationship.objects.get(user_id=self.student.id, course__id=self.course.id).role,
                         self.data["role"])

    def test_edit_user_as_invalid_coordinator(self):
        """
        Test to verify a coordinator from another course is unable to edit a user.
        """
        self.client.force_login(self.coordinator_2)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserCourseRelationship.objects.get(user_id=self.student.id, course__id=self.course.id).role,
                            self.data["role"])

    def test_edit_user_as_assistant(self):
        """
        Test to verify a assistant is unable to edit a user.
        """
        self.client.force_login(self.assistant)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserCourseRelationship.objects.get(user_id=self.student.id, course__id=self.course.id).role,
                            self.data["role"])

    def test_edit_user_as_student(self):
        """
        Test to verify a student is unable to edit a user.
        """
        self.client.force_login(self.student)
        self.assertEqual(self.edit_user().status_code, 403)
        self.assertNotEqual(UserCourseRelationship.objects.get(user_id=self.student.id, course__id=self.course.id).role,
                            self.data["role"])
