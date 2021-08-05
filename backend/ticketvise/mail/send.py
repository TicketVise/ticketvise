import logging
from ticketvise.models.inbox import MailSecurity
import threading

from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class EmailThread(threading.Thread):

    def __init__(self, message, smtp_host, smtp_port, smtp_username, smtp_password, smtp_security):
        self.message = message
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_security = smtp_security

        threading.Thread.__init__(self)

    def run(self):
        print("smtp", self.smtp_host, self.smtp_port, self.smtp_username, self.smtp_password, self.smtp_security)

        with get_connection(host=self.smtp_host, port=self.smtp_port, username=self.smtp_username,
                            password=self.smtp_password, use_tls=self.smtp_security == MailSecurity.TLS,
                            use_ssl=self.smtp_security == MailSecurity.STARTTLS) as connection:
            self.message.connection = connection
            print(self.smtp_host, self.smtp_port, self.smtp_username, self.smtp_password, self.smtp_security)
            self.message.send()


def send_mail_template(subject, sender, to, template, headers, context, smtp_host, smtp_port, smtp_username, smtp_password, smtp_security):
    """
    This function sends an email to a user using a specified template.

    :param str subject: Subject of the email.
    :param str to: Email address of the recipient.
    :param str template: Template file to use, located in ``/templates/email``.
    :param dict context: Dictionary of variables to be used in the email.

    :return: True if the mail Celery task has been started, false otherwise.
    :rtype: bool
    """
    logging.info(f"Sending email from '{sender}' to '{to}'")
    
    html_message = render_to_string(f"email/{template}.html", context)
    plain_message = strip_tags(html_message)

    email = EmailMultiAlternatives(
        subject=subject, body=plain_message, from_email=sender, to=[to], headers=headers)
    email.attach_alternative(html_message, "text/html")
    EmailThread(email, smtp_host, smtp_port, smtp_username,
                smtp_password, smtp_security).start()
