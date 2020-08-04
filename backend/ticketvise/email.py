"""
Email
-------------------------------
Used to send an email to a user.
"""
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from celery.decorators import task
from django.core.mail import send_mail


def send_email(subject, to, template, context):
    """
    This function sends an email to a user using a specified template.

    :param str subject: Subject of the email.
    :param str to: Email address of the recipient.
    :param str template: Template file to use, located in ``/templates/email``.
    :param dict context: Dictionary of variables to be used in the email.

    :return: True if the mail Celery task has been started, false otherwise.
    :rtype: bool
    """
    if settings.SEND_MAIL:
        html_message = render_to_string(f"email/{template}.html", context)
        plain_message = strip_tags(html_message)
        from_email = settings.GLOBAL_SETTINGS["email_address"]

        mail_sender.delay(subject, plain_message, from_email, [to], html_message)

        return True

    return False


@task
def mail_sender(subject, plain_message, from_email, to, html_message):
    """
    This function sends an email to a user through a Celery task using a specified template.

    :param str subject: Subject of the email.
    :param str plain_message: The plain version of the message.
    :param str from_email: The sender of the email.
    :param str to: The recipient of the email.
    :param str html_message: The html version of the message.

    :return: None.
    """
    send_mail(subject, plain_message, from_email, to, html_message=html_message)
