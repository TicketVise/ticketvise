from django.test import TestCase

from ticketvise.utils import get_text_color


class UtilsTestCase(TestCase):
    def setUp(self):
        """
        Initialize the testing variables.
        """
        self.context = {}

    def test_get_text_light_background(self):
        self.assertTrue(get_text_color("#ffffff"), "#000000")

    def test_get_text_dark_background(self):
        self.assertTrue(get_text_color("#000000"), "#ffffff")
