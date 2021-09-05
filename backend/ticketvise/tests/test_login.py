"""
Test Login
-------------------------------
This file tests the login page of the website.
"""

from django.test import TestCase
from rest_framework.test import APIClient

from ticketvise.models.user import User


class LoginTestCase(TestCase):

    def setUp(self):
        """
        Setup for each of these tests.
        We create a client and also a dummy test user.

        :return: None.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="root", email="root@ticketvise.com", password="correct"
        )

    def test_login(self):
        """
        Testing the login functionality.
        And check that we get redirected after logging in to the dashboard.

        :return: None.
        """
        response = self.client.post("/api/login", {"username": "root", "password": "correct"}, follow=True)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        # Also test putting in the wrong password.
        response = self.client.post("/api/login", {"username": "root", "password": "wrong"}, follow=True)
        self.assertEqual(response.status_code, 401)

        # Also test putting in no password.
        response = self.client.post("/api/login", {"username": "root", "password": ""}, follow=True)
        self.assertEqual(response.status_code, 400)

        # Also test putting in no username.
        response = self.client.post("/api/login", {"username": "", "password": "correct"}, follow=True)
        self.assertEqual(response.status_code, 400)

        # Also test putting in nothing.
        response = self.client.post("/api/login", {}, follow=True)
        self.assertEqual(response.status_code, 400)
