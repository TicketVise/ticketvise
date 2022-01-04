from ticketvise.models.utils import MailSecurity
from ticketvise.mail import oauth_2_auth_base64
import logging
import threading

from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.utils import DNS_NAME
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class OAuthCompatibleEmailBackend(EmailBackend):
    """
    A wrapper that manages the SMTP network connection.
    """
    def __init__(self, use_oauth2=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_oauth2=use_oauth2

    def open(self):
        """
        Extension of django.core.mail.backends.smtp.EmailBackend.open
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        # If local_hostname is not specified, socket.getfqdn() gets used.
        # For performance, we use the cached FQDN for local_hostname.
        connection_params = {'local_hostname': DNS_NAME.get_fqdn()}
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
        if self.use_ssl:
            connection_params.update({
                'keyfile': self.ssl_keyfile,
                'certfile': self.ssl_certfile,
            })
        try:
            self.connection = self.connection_class(self.host, self.port, **connection_params)

            # TLS/SSL are mutually exclusive, so only attempt TLS over
            # non-secure connections.
            if not self.use_ssl and self.use_tls:
                self.connection.starttls(keyfile=self.ssl_keyfile, certfile=self.ssl_certfile)
                self.connection.ehlo_or_helo_if_needed()
            if self.username and self.password:
                if self.use_oauth2:
                    auth_string = oauth_2_auth_base64(self.username, self.password)
                    self.connection.auth("XOAUTH2", lambda: auth_string)
                else:
                    self.connection.login(self.username, self.password)
            return True
        except OSError:
            if not self.fail_silently:
                raise

class EmailThread(threading.Thread):

    def __init__(self, message, smtp_host, smtp_port, smtp_username, smtp_password, smtp_security, smtp_use_oauth2):
        self.message = message
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_security = smtp_security
        self.smtp_use_oauth2 = smtp_use_oauth2

        threading.Thread.__init__(self)

    def run(self):
        with get_connection(host=self.smtp_host, port=self.smtp_port, username=self.smtp_username,
                            password=self.smtp_password, use_tls=self.smtp_security == MailSecurity.TLS,
                            use_ssl=self.smtp_security == MailSecurity.STARTTLS,
                            use_oauth2=self.smtp_use_oauth2) as connection:
            self.message.connection = connection
            self.message.send()


def send_mail_template(subject, sender, to, template, headers, context, smtp_host, smtp_port, smtp_username, smtp_password, smtp_security, smtp_use_oauth2):
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
                smtp_password, smtp_security, smtp_use_oauth2).start()
