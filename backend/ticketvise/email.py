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
from aiosmtpd.controller import Controller
from email_reply_parser import EmailReplyParser

def send_ticket_shared_mail(ticket, to):
    send_mail_template(
        f"#{ticket.ticket_inbox_id} - A ticket has been shared with you",
        to.email,
        "ticket_shared",
        {"X-Ticket-Id": ticket.id},
        {"ticket": ticket}
    )

def send_ticket_assigned_mail(ticket, to):
    send_mail_template(
        f"#{ticket.ticket_inbox_id} - A ticket has been assigned to you",
        to.email,
        "ticket_assigned",
        {"X-Ticket-Id": ticket.id},
        {"ticket": ticket}
    )

def send_mentioned_mail(comment, to):
    send_mail_template(
        f"#{comment.ticket.ticket_inbox_id} - You have been mentioned by {comment.author.get_full_name()} ",
        to.email,
        "ticket_mention",
        {"X-Ticket-Id": comment.ticket.id},
        {"ticket": comment.ticket}
    )

def send_ticket_status_changed_mail(ticket, to):
    send_mail_template(
        f"#{ticket.ticket_inbox_id} - Status has been changed to {ticket.status}",
        to.email,
        "ticket_status_change",
        {"X-Ticket-Id": ticket.id},
        {"ticket": ticket}
    )


def send_ticket_new_reply_mail(ticket, comment, to):
    send_mail_template(
        f"#{ticket.ticket_inbox_id} - {comment.author.get_full_name()} has send a reply",
        to.email,
        "ticket_reply",
        {"X-Ticket-Id": ticket.id},
        {"ticket": ticket}
    )

def send_ticket_reminder_email(ticket, to):
    alert_days = ticket.course.alert_coordinator_unanswered_days
    send_mail_template(
        f"#{ticket.ticket_inbox_id} - Ticket has been unanswered for {alert_days} days",
        to.email,
        "ticket_reminder",
        {"X-Ticket-Id": ticket.id},
        {"ticket": ticket}
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
    if settings.SEND_MAIL:
        html_message = render_to_string(f"email/{template}.html", context)
        plain_message = strip_tags(html_message)
        from_email = settings.GLOBAL_SETTINGS["email_address"]


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
