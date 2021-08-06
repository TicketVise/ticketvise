"""
Test LTI
-------------------------------
This file tests the LTI integration with the website.
"""
import math
import time
from urllib.parse import urlencode

import oauthlib.oauth1.rfc5849.signature as oauth1
from django.test import TestCase
from rest_framework.test import APIClient

from ticketvise import settings
from ticketvise.models.inbox import Inbox, InboxSection, InboxUserSection
from ticketvise.models.user import User


class LtiTestCase(TestCase):
    def setUp(self):
        """
        Setup for each of these tests.
        We create a client and also a dummy test user.

        :return: None.
        """
        self.client = APIClient()
        self.data = {
            "context_id": "2734dde21bed2288f65c7513a78f1653415da235",
            "context_label": "Test_code",
            "context_title": "Testcurses",
            "custom_course_name": "100",
            "custom_email": "test@ticketvise.com",
            "custom_image_url": "https://uvadlo-tes.instructure.com/images/messages/avatar-50.png",
            "custom_user_full_name": "Test persoon",
            "custom_username": "test",
            "custom_section_ids": "1234",
            "roles": "Instructor,urn:lti:instrole:ims/lis/Administrator",
            "user_id": "1234567890"
        }

    def sign_data(self, method, path, data):
        initial_data = {
            "oauth_consumer_key": settings.LTI_KEY,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_nonce": "nonce",
            "oauth_timestamp": str(math.floor(time.time())),
            "oauth_version": "1.0"
        }

        data = {**initial_data, **data}

        params = oauth1.collect_parameters(
            body=data,
            exclude_oauth_signature=True,
            with_realm=False
        )

        norm_params = oauth1.normalize_parameters(params)

        base_string = oauth1.signature_base_string(
            method,
            'http://testserver' + path,
            norm_params
        )

        signature = oauth1.sign_hmac_sha1(
            base_string,
            settings.LTI_SECRET,
            ''  # resource_owner_secret - not used
        )

        data["oauth_signature"] = signature

        return urlencode(data)

    def test_login_with_new_user(self):
        """
        Login with the created user and test the response.

        :return: None.
        """

        signed_data = self.sign_data("POST", "/lti", self.data)
        response = self.client.post("/lti", signed_data, follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 302)

    def test_lti_invalid_key(self):
        """
        Launch LTI with no key.

        :return: None.
        """
        self.data["oauth_consumer_key"] = "None"
        signed_data = self.sign_data("POST", "/lti", self.data)

        self.client.request()

        response = self.client.post("/lti", signed_data, follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 403)

    def test_lti_invalid_timestamp(self):
        """
        Launch LTI with invalid timestamp.

        :return: None.
        """
        data = self.data
        data["oauth_timestamp"] = "5"
        signed_data = self.sign_data("POST", "/lti", self.data)

        response = self.client.post("/lti", signed_data, follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 403)

    def test_lti_no_inbox(self):
        """
        Launch LTI without active inbox.

        :return: None.
        """
        data = self.data
        data["roles"] = "teachingassistant"
        signed_data = self.sign_data("POST", "/lti", self.data)

        response = self.client.post("/lti", signed_data, follow=True,
                                    content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 404)

    def test_lti_assistant(self):
        """
        Launch LTI with assistant role.

        :return: None.
        """
        signed_data = self.sign_data("POST", "/lti", self.data)

        # Create inbox.
        response1 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")

        self.assertEqual(response1.status_code, 302)

        # Login as assistant.
        self.data["roles"] = "teachingassistant"

        signed_data = self.sign_data("POST", "/lti", self.data)

        response2 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")
        self.assertEqual(response2.status_code, 302)

    def test_lti_ticket_view(self):
        """
        Launch LTI going to the ticket view.

        :return: None.
        """
        # Create inbox.
        self.data["roles"] = "instructor"
        signed_data = self.sign_data("POST", "/lti", self.data)

        response1 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")
        self.assertEqual(response1.status_code, 302)

        # Create student account.
        self.data["roles"] = "learner"
        signed_data = self.sign_data("POST", "/lti", self.data)

        response2 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")
        self.assertEqual(response2.status_code, 302)

        # Let us check if we login and go to the ticket view.
        response3 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")
        self.assertEqual(response3.status_code, 302)

    def test_lti_sections(self):
        """
        Launch LTI and check if section ids exist.

        :return: None
        """
        # Create inbox.
        self.data["custom_section_ids"] = "1234"
        self.data["roles"] = "instructor"
        signed_data = self.sign_data("POST", "/lti", self.data)

        response1 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")
        self.assertEqual(response1.status_code, 302)

        inbox = Inbox.objects.get(code=self.data["context_label"])
        user = User.objects.get(lti_id=self.data["user_id"])

        section = InboxSection.objects.get(code="1234", inbox=inbox)
        self.assertIsNotNone(section)
        inbox_user_section = InboxUserSection.objects.get(section=section, user=user)
        self.assertIsNotNone(inbox_user_section)

        # Update sections
        self.data["custom_section_ids"] = "1234,4567,9876"
        signed_data = self.sign_data("POST", "/lti", self.data)

        response2 = self.client.post("/lti", signed_data, follow=True,
                                     content_type="application/x-www-form-urlencoded")
        self.assertEqual(response2.status_code, 302)

        section = InboxSection.objects.get(code="1234", inbox=inbox)
        self.assertIsNotNone(section)
        inbox_user_section = InboxUserSection.objects.get(section=section, user=user)
        self.assertIsNotNone(inbox_user_section)

        section = InboxSection.objects.get(code="4567", inbox=inbox)
        self.assertIsNotNone(section)
        inbox_user_section = InboxUserSection.objects.get(section=section, user=user)
        self.assertIsNotNone(inbox_user_section)

        section = InboxSection.objects.get(code="9876", inbox=inbox)
        self.assertIsNotNone(section)
        inbox_user_section = InboxUserSection.objects.get(section=section, user=user)
        self.assertIsNotNone(inbox_user_section)
