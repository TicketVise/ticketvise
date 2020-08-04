from django.urls import reverse

from ticketvise.tests.course.utils import CourseTestCase


class BaseTestCase(CourseTestCase):
    def test_course_assistant_403(self):
        """
        Test to verify that a assistant is unable to access course related pages. Pages should return a HTTP 403
        status code when a assistant tries to access a page.
        """
        self.client.force_login(self.assistant)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args), follow=True)
            self.assertEqual(response.status_code, 403)

    def test_course_coordinator_200(self):
        """
        Test to verify that a coordinator is able to access course related pages. Pages should return a HTTP 200
        status code when a coordinator tries to access a page.
        """
        self.client.force_login(self.coordinator)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_course_student_403(self):
        """
        Test to verify that a student is unable to access course related pages. Pages should return a HTTP 403
        status code when a student tries to access a page.
        """
        self.client.force_login(self.student)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args), follow=True)
            self.assertEqual(response.status_code, 403)

    def test_course_anonymous_redirect_login(self):
        """
        A not logged in user should be redirected to the login page with a referral.
        """
        for template_name, args in self.template_names:
            url = reverse(template_name, args=args)
            response = self.client.get(url, follow=True)
            self.assertRedirects(response, '/login/?next=' + url, status_code=302,
                                 target_status_code=200, fetch_redirect_response=True)

    def test_coordinator_not_in_course(self):
        """
        Test to verify that a coordinator which is not associated with the course is unable to access course related
        pages. Pages should return a HTTP 403 status code when a coordinator from a other course tries to access a page.
        """
        self.client.force_login(self.coordinator_2)

        for template_name, args in self.template_names:
            response = self.client.get(reverse(template_name, args=args), follow=True)
            self.assertEqual(response.status_code, 403)

    def test_pagination_not_numeric(self):
        """
        Test to verify that when a path variable is not a numeric value, no unexpected behaviour occurs.
        """
        self.client.force_login(self.coordinator)

        for template_name, args in self.template_names:
            url = reverse(template_name, args=args).replace("1", "1a")
            response = self.client.get(url, follow=True)
            self.assertEqual(response.status_code, 404)
