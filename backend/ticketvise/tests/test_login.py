"""
Test Login
-------------------------------
This file tests the login page of the website.
"""
from urllib.parse import urlencode

from django.test import TestCase, Client
from django.urls import reverse

from ticketvise.models.inbox import Inbox
from ticketvise.models.user import User


class LoginTestCase(TestCase):
    def setUp(self):
        """
        Setup for each of these tests.
        We create a client and also a dummy test user.

        :return: None.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="root", email="root@ticketvise.com", password="correct"
        )

    def test_show_page(self):
        """
        Make sure we can get the login page.

        :return: None.
        """
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_login_page(self):
        """
        Check that we get redirected to the login page.

        :return: None.
        """
        inbox = Inbox.objects.create(name="name", code="code")
        response = self.client.get(reverse("ticket_overview", args=(inbox.id,)))
        self.assertRedirects(response, "/login/?next=%2Finboxes%2F{}%2Ftickets".format(inbox.id))

    # def test_preserve_username_when_login_failed(self):
    #     """
    #     Check that the username is preserved when the login fails.

    #     :return: None.
    #     """
    #     data = {
    #         "username": "fout",
    #         "password": "ook fout"
    #     }
    #     response = self.client.post('/login/', urlencode(data), follow=True,
    #                                 content_type="application/x-www-form-urlencoded")
    #     self.assertContains(response, "<input name=\"username\" placeholder=\"12345678\" class=\"input\" "
    #                                   "required value=\"fout\">", html=True)

    def test_login(self):
        """
        Testing the login functionality.
        And check that we get redirected after logging in to the dashboard.

        :return: None.
        """
        response = self.client.post("/login/", {"username": "root", "password": "correct"}, follow=True)
        self.assertRedirects(response, "/inboxes")

        self.client.logout()

        # Also test putting in the wrong password.
        response = self.client.post("/login/", {"username": "root", "password": "wrong"}, follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

        # Also test putting in no password.
        response = self.client.post("/login/", {"username": "root", "password": ""}, follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

        # Also test putting in no username.
        response = self.client.post("/login/", {"username": "", "password": "correct"}, follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

        # Also test putting in nothing.
        response = self.client.post("/login/", {}, follow=True)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_logout(self):
        """
        Test that we can also logout and are being
        redirected back to the login page.

        :return: None.
        """
        self.client.login(username="root", password="test1234")
        response = self.client.post("/logout/", follow=True)
        self.assertRedirects(response, "/login/?next=%2F")
