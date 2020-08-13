"""
Email
-------------------------------
Used to send an email to a user.
"""
from email import policy
from email.parser import BytesParser

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
from aiosmtpd.controller import Controller
from email_reply_parser import EmailReplyParser

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


class SmtpServer:

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # if not address.endswith('@example.com'):
        #     return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)

        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos

        message = BytesParser(policy=policy.default).parsebytes(envelope.content)
        body = message.get_body(('plain',))
        if body:
            content = body.get_content()
            reply = EmailReplyParser.parse_reply(content)

        return '250 OK'

    def start(self):
        self.controller = Controller(self, hostname="127.0.0.1", port=settings.SMTP_INBOUND_PORT)
        self.controller.start()
        print("SMTP server started on port {}".format(settings.SMTP_INBOUND_PORT))

    def stop(self):
        self.controller.stop()

