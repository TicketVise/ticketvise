"""
Email
-------------------------------
Used to send an email to a user.
"""
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import send_mail
from aiosmtpd.controller import Controller
import email

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

    def get_body(self, message):
        msg = email.message_from_bytes(message)
        msg_subject = msg["Subject"]
        if subject in msg_subject:
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    type = part.get_content_type()
                    disp = str(part.get('Content-Disposition'))
                    # look for plain text parts, but skip attachments
                    if type == 'text/plain' and 'attachment' not in disp:
                        charset = part.get_content_charset()
                        # decode the base64 unicode bytestring into plain text
                        body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                        # if we've found the plain/text part, stop looping thru the parts
                        break
            else:
                # not multipart - i.e. plain text, no attachments
                charset = msg.get_content_charset()
                body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
            messages.append({'num': num, 'body': body})
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # if not address.endswith('@example.com'):
        #     return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)

        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        peer = session.peer
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        data = envelope.content  # type: bytes

        message = email.message_from_bytes(envelope.content)

        return '250 OK'

    def start(self):
        self.controller = Controller(self, hostname="127.0.0.1", port=settings.SMTP_INBOUND_PORT)
        self.controller.start()
        print("SMTP server started on port {}".format(settings.SMTP_INBOUND_PORT))

    def stop(self):
        self.controller.stop()

