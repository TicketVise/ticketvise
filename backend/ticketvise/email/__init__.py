"""
Email
-------------------------------
Used to send an email to a user.
"""
import threading

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from ticketvise import settings


class EmailThread(threading.Thread):

    def __init__(self, message):
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        self.message.send()


def send_mail_template(subject, to, template, headers, context):
    """
    This function sends an email to a user using a specified template.

    :param str subject: Subject of the email.
    :param str to: Email address of the recipient.
    :param str template: Template file to use, located in ``/templates/email``.
    :param dict context: Dictionary of variables to be used in the email.

    :return: True if the mail Celery task has been started, false otherwise.
    :rtype: bool
    """
    html_message = render_to_string(f"email/{template}.html", context)
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_FROM

    email = EmailMultiAlternatives(subject=subject, body=plain_message, from_email=from_email, to=[to], headers=headers)
    email.attach_alternative(html_message, "text/html")
    EmailThread(email).start()
