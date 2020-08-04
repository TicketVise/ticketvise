"""
Test Profile
-------------------------------
This file tests the profile specific functionality on the profile page.
"""
from urllib.parse import urlencode

from django.test import TestCase, Client

from ticketvise.models.user import User


class ProfileTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.student = User.objects.create_user(
            username="student", email="root@ticketvise.com", password="test12345", is_staff=False,
        )

    def test_delete_account(self):
        """
        Test if the delete account button deletes the account and redirects to the homepage after a logout.
        :return:
        """
        self.client.login(username="student", password="test12345")

        self.assertTrue(self.student.has_usable_password())

        data = {"action": "delete_account"}
        response = self.client.post("/profile", urlencode(data), follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertRedirects(response, "/login/?next=%2F")

        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

        self.assertFalse(User.objects.filter(email="root@ticketvise.com").count())
