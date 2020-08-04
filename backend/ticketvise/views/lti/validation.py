import time

import oauthlib.oauth1.rfc5849.signature as oauth
from django import forms
from django.core.exceptions import ValidationError
from oauthlib.common import Request

from ticketvise import settings


class LtiLaunchForm(forms.Form):
    """
    Specifies the fields and valid requirements of the form for an LtiLaunch.
    """

    oauth_consumer_key = forms.CharField()
    oauth_token = forms.CharField()
    oauth_nonce = forms.CharField()
    oauth_timestamp = forms.IntegerField()
    oauth_signature_method = forms.CharField()
    oauth_version = forms.FloatField()
    oauth_signature = forms.CharField()
    #: The id of the user.
    user_id = forms.CharField()
    #: The full name of the user.
    custom_user_full_name = forms.CharField()
    #: The custom username of the user.
    custom_username = forms.CharField()
    #: The custom mail of the user.
    custom_email = forms.EmailField()
    #: The profile picture of the user.
    custom_image_url = forms.URLField()
    #: The name of the course of the user.
    custom_course_name = forms.CharField()
    #: The code of the course.
    context_label = forms.CharField()
    #: The role of user in the course.
    roles = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LtiLaunchForm, self).__init__(*args, **kwargs)

    def clean_oauth_consumer_key(self):
        """
        Check whether there is a consumer key and whether it is the right key.

        :return: The identity key of the consumer.
        :rtype: str

        :raises ValidationError: When the key is invalid.
        """
        oauth_consumer_key = self.cleaned_data["oauth_consumer_key"]

        if oauth_consumer_key != settings.LTI_KEY:
            raise ValidationError("Invalid consumer key")

        return oauth_consumer_key

    def clean_oauth_timestamp(self):
        """
        Check whether the request is not older than 5 minutes.
        Otherwise, the link has expired.

        :return: Timestamp of the request.
        :rtype: int

        :raises ValidationError: When authentication expired.
        """
        oauth_timestamp = self.cleaned_data["oauth_timestamp"]
        timeout_duration = 5 * 60

        if oauth_timestamp + timeout_duration < time.time():
            raise ValidationError("Authentication expired")

        return oauth_timestamp

    def clean_oauth_signature_method(self):
        oauth_signature_method = self.cleaned_data["oauth_signature_method"]

        if oauth_signature_method != "HMAC-SHA1":
            raise ValidationError("Invalid signature method")

        return oauth_signature_method

    def clean_oauth_version(self):
        oauth_version = self.cleaned_data["oauth_version"]

        if oauth_version != 1.0:
            raise ValidationError("Unsupported OAuth version")

        return oauth_version

    def clean_oauth_signature(self):
        oauth_request = Request(self.request.build_absolute_uri(), self.request.method, self.request.POST)
        oauth_request.signature = self.cleaned_data["oauth_signature"]
        oauth_request.params = [(k, v) for k, v in self.request.POST.items() if k != "oauth_signature"]

        if not oauth.verify_hmac_sha1(oauth_request, settings.LTI_SECRET):
            raise ValidationError("Invalid signature")

        return self.cleaned_data["oauth_signature"]

    def is_valid(self):
        """
        Check whether the form is valid.

        :return: Whether the form is valid.
        :rtype: bool
        """
        return super().is_valid()
