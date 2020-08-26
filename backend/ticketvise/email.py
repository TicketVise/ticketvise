"""
Email
-------------------------------
Used to send an email to a user.
"""
from email import policy
from email.parser import BytesParser
import threading

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from aiosmtpd.controller import Controller
from email_reply_parser import EmailReplyParser

from ticketvise import settings


class EmailThread(threading.Thread):

    def __init__(self, message):
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        self.message.send()


def send_ticket_shared_mail(ticket, to):
    title = f"#{ticket.ticket_inbox_id} - A ticket has been shared with you"

    send_mail_template(
        title,
        to.email,
        "comments",
        {
            "Message-Id": f"<{ticket.reply_message_id}@{settings.DOMAIN}>",
        },
        {
            "title": title,
            "ticket": ticket,
            "comments": ticket.comments.filter(is_reply=True)
        }
    )


def send_ticket_assigned_mail(ticket, to):
    title = f"#{ticket.ticket_inbox_id} - A ticket has been assigned to you"

    send_mail_template(
        title,
        to.email,
        "comments",
        {
            "Message-Id": f"<{ticket.reply_message_id}@{settings.DOMAIN}>",
        },
        {
            "title": title,
            "ticket": ticket,
            "comments": ticket.comments.filter(is_reply=True)
        }
    )


def send_mentioned_mail(comment, to):
    title = f"#{comment.ticket.ticket_inbox_id} - You have been mentioned by {comment.author.get_full_name()}"

    send_mail_template(
        title,
        to.email,
        "comments",
        {
            "Message-Id": f"<{comment.ticket.comment_message_id}@{settings.DOMAIN}>",
        },
        {
            "title": title,
            "ticket": comment.ticket,
            "comments": comment.ticket.comments.filter(is_reply=False)
        }
    )


def send_ticket_status_changed_mail(ticket, to):
    title = f"#{ticket.ticket_inbox_id} - Status has been changed to {ticket.status}"

    send_mail_template(
        title,
        to.email,
        "comments",
        {
            "Message-Id": f"<{ticket.reply_message_id}@{settings.DOMAIN}>",
        },
        {
            "title": title,
            "ticket": ticket,
            "comments": ticket.comments.filter(is_reply=True)
        }
    )


def send_ticket_new_reply_mail(ticket, comment, to):
    title = f"#{ticket.ticket_inbox_id} - {comment.author.get_full_name()} has send a reply"

    send_mail_template(
        title,
        to.email,
        "comments",
        {
            "Message-Id": f"<{ticket.reply_message_id}@{settings.DOMAIN}>",
        },
        {
            "title": title,
            "ticket": ticket,
            "comments": ticket.comments.filter(is_reply=True)
        }
    )


def send_ticket_reminder_email(ticket, to):
    alert_days = ticket.course.alert_coordinator_unanswered_days
    title = f"#{ticket.ticket_inbox_id} - Ticket has been unanswered for {alert_days} days"

    send_mail_template(
        title,
        to.email,
        "comments",
        {
            "Message-Id": f"<{ticket.reply_message_id}@{settings.DOMAIN}>",
        },
        {
            "title": title,
            "ticket": ticket,
            "comments": ticket.comments.filter(is_reply=True)
        }
    )


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


class SmtpServer:

    def __init__(self) -> None:
        self.controller = Controller(self, hostname="127.0.0.1", port=settings.SMTP_INBOUND_PORT)
        super().__init__()

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
        try:
            self.controller.stop()
        except:
            pass

        try:
            self.controller.start()
            print("SMTP server started on port {}".format(settings.SMTP_INBOUND_PORT))
        except:
            pass

    def stop(self):
        self.controller.stop()
