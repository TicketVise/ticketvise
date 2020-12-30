from django.urls import reverse

from ticketvise.tests.inbox.utils import InboxTestCase


class BaseTestCase(InboxTestCase):

    def test_inbox_assistant_403(self):
        """
        Test to verify that a assistant is unable to access inbox related pages. Pages should return a HTTP 403
        status code when a assistant tries to access a page.
        """
        self.client.force_authenticate(self.assistant)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args))
            self.assertEqual(response.status_code, 403)

    def test_inbox_coordinator_200(self):
        """
        Test to verify that a coordinator is able to access inbox related pages. Pages should return a HTTP 200
        status code when a coordinator tries to access a page.
        """
        self.client.force_authenticate(self.coordinator)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args))
            self.assertEqual(response.status_code, 200)

    def test_inbox_student_403(self):
        """
        Test to verify that a student is unable to access inbox related pages. Pages should return a HTTP 403
        status code when a student tries to access a page.
        """
        self.client.force_authenticate(self.student)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args))
            self.assertEqual(response.status_code, 403)

    def test_inbox_anonymous_redirect_login(self):
        """
        A not logged in user should be redirected to the login page with a referral.
        """
        for template_name, args in self.template_names:
            url = reverse(template_name, args=args)
            response = self.client.get(url, follow=False)
            self.assertEqual(response.status_code, 401)

    def test_coordinator_not_in_inbox(self):
        """
        Test to verify that a coordinator which is not associated with the inbox is unable to access inbox related
        pages. Pages should return a HTTP 403 status code when a coordinator from a other inbox tries to access a page.
        """
        self.client.force_authenticate(self.coordinator_2)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args))
            self.assertEqual(response.status_code, 403)

    def test_pagination_not_numeric(self):
        """
        Test to verify that when a path variable is not a numeric value, no unexpected behaviour occurs.
        """
        self.client.force_authenticate(self.coordinator)

        for template_name, args in self.template_names:
            url = reverse(template_name, args=args).replace("1", "1a")
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 404)

    def test_get_coordinator(self):
        """
        Test if the get_coordinator function return the coordinator
        """
        self.assertEqual(self.inbox.get_coordinator(), self.coordinator)