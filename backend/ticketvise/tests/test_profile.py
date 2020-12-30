from django.test import TestCase, Client
from rest_framework.test import APIClient

from ticketvise.models.user import User


class AccountTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.guest = User.objects.create(username="guest", password="test12345", email="guest@ticketvise.com")
        self.ta = User.objects.create(username="ta", password="test12345", email="ta@ticketvise.com")
        self.manager = User.objects.create(username="manager", password="test12345", email="manager@ticketvise.com")
        self.superuser = User.objects.create(username="superuser", password="test12345",
                                             email="superuser@ticketvise.com", is_staff=True)
        self.users = [self.guest, self.ta, self.manager, self.superuser]

    def test_ticket_page_200(self):
        """
        Authorized users should see their own account.

        :return: None.
        """
        for user in self.users:
            self.client.force_authenticate(user)
            response = self.client.get("/account")
            self.assertEqual(response.status_code, 200)

    def test_ticket_page_401(self):
        """
        Unauthorized users should be redirected to the login page. When logged in
        it should redirect to the account.

        :return: None.
        """
        response = self.client.get("/account")
        self.assertRedirects(response, '/login/?next=/account')

    def test_correct_template_used(self):
        """
        The account page should use the account.html template.

        :return: None.
        """
        self.client.force_login(self.guest)
        response = self.client.get("/account")
        self.assertTemplateUsed(response, 'account.html')
