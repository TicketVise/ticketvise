from django.test import TestCase, Client

from ticketvise.models.user import User
from ticketvise.tests.utils import create_label, create_course


class CourseTestCase(TestCase):
    def setUp(self):
        """
        Set up the database for the course related tests.
        """
        self.client = Client()
        self.student = User.objects.create_user(
            username="student", email="root@ticketvise.com", password="test12345", is_staff=False
        )
        self.student.set_password("test12345")
        self.student.save()

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

        self.course = create_course("course_1_name", "course_1_code")
        self.course_2 = create_course("course_2_name", "course_2_code")

        self.student.add_course(self.course, User.Roles.STUDENT)
        self.student.add_course(self.course_2, User.Roles.STUDENT)
        self.assistant.add_course(self.course, User.Roles.ASSISTANT)
        self.coordinator.add_course(self.course, User.Roles.COORDINATOR)
        self.coordinator_2.add_course(self.course_2, User.Roles.COORDINATOR)
        self.label = create_label(course=self.course)
        self.label_2 = create_label(course=self.course_2)

        self.template_names = [
            ("course_user", (self.course.id, self.student.id)),
            ("course_users", (self.course.id,)),
            ("course_labels", (self.course.id,)),
            ("course_settings", (self.course.id,)),
            ("create_course_label", (self.course.id,)),
            ("course_statistics", (self.course.id,)),
            ("edit_course_label", (self.course.id, self.label.id)),
            ("delete_course_label", (self.course.id, self.label.id)),
            ("course_user_delete", (self.course.id, self.student.id)),
        ]
