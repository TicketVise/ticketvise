import time

import oauthlib.oauth1.rfc5849.signature as oauth
from django import forms
from django.core.exceptions import ValidationError
from oauthlib.common import Request

from ticketvise import settings


class LtiLaunchForm(forms.Form):
    """
    Specifies the fields and valid requirements of the form for an LTI launch.
    """

    #: OAuth related parameters
    oauth_consumer_key = forms.CharField()
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
    #: The name of the inbox of the user.
    custom_course_name = forms.CharField()
    #: The code of the inbox.
    context_label = forms.CharField()
    #: The role of user in the inbox.
    roles = forms.CharField()
    #: The section ids of user in the inbox.
    custom_section_ids = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LtiLaunchForm, self).__init__(*args, **kwargs)

    def clean_oauth_consumer_key(self):
        """
        Cleans and validates the OAuth consumer key. The check ensures the correct key is used. This key is agreed upon
        by both parties; the LTI consumer en LTI provider.
        """
        oauth_consumer_key = self.cleaned_data["oauth_consumer_key"]

        if oauth_consumer_key != settings.LTI_KEY:
            raise ValidationError("Invalid consumer key")

        return oauth_consumer_key

    def clean_oauth_timestamp(self):
        """
        Cleans and validates the OAuth timestamp. The check ensures that the request is not older than 5 minutes.
        """
        oauth_timestamp = self.cleaned_data["oauth_timestamp"]
        timeout_duration = 5 * 60

        if oauth_timestamp + timeout_duration < time.time():
            raise ValidationError("Authentication expired")

        return oauth_timestamp

    def clean_oauth_signature_method(self):
        """
        Cleans and validates the signature hashing method. Currently only HMAC-SHA1 is supported, which is widely
        supported and used by LTI providers.
        """
        oauth_signature_method = self.cleaned_data["oauth_signature_method"]

        if oauth_signature_method != "HMAC-SHA1":
            raise ValidationError("Invalid signature method")

        return oauth_signature_method

    def clean_oauth_version(self):
        """
        Cleans and validates the OAuth version. Since LTI 1.0 supports only OAuth 1.0, this is the only valid version.
        """
        oauth_version = self.cleaned_data["oauth_version"]

        if oauth_version != 1.0:
            raise ValidationError("Unsupported OAuth version")

        return oauth_version

    def clean_oauth_signature(self):
        """
        Cleans and validates the 'oauth signature'. The signature is verified by calculating the hash (using the
        algorithm specified in 'oauth_signature_method') of the URL, METHOD and BODY. After the calculation the
        signature is compared with the 'oauth_signature' to check if they match. When the signatures match we can
        assure that the request is from a authorized entity.
        """
        oauth_request = Request(self.request.build_absolute_uri(), self.request.method, self.request.POST)
        oauth_request.signature = self.cleaned_data["oauth_signature"]
        oauth_request.params = [(k, v) for k, v in self.request.POST.items() if k != "oauth_signature"]

        if not oauth.verify_hmac_sha1(oauth_request, settings.LTI_SECRET):
            raise ValidationError("Invalid signature, URL: {}, method: {}".format(
                self.request.build_absolute_uri(),
                self.request.method))

        return self.cleaned_data["oauth_signature"]
