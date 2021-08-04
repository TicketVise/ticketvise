from ticketvise.models.inbox import MailSecurity
from django.core.mail import get_connection
from django.db import models
from model_utils.managers import InheritanceManager

from ticketvise import settings
from ticketvise.mail.send import send_mail_template


class Notification(models.Model):
    objects = InheritanceManager()
    receiver = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def author(self):
        raise NotImplementedError

    @property
    def content(self):
        raise NotImplementedError

    @property
    def inbox(self):
        raise NotImplementedError

    def get_email_subject(self):
        return f"#{self.ticket.ticket_inbox_id} - {self.content}"

    def get_email_comments(self):
        return self.ticket.comments.filter(is_reply=True)

    def get_message_id(self):
        return self.ticket.reply_message_id

    def send_mail(self):
        print("send to", self.receiver.email)
        send_mail_template(
            self.get_email_subject(),
            self.ticket.inbox.smtp_username if self.ticket.inbox.email_enabled else settings.EMAIL_FROM,
            self.receiver.email,
            "comments",
            {
                "Message-Id": f"<{self.get_message_id()}@{settings.DOMAIN}>",
            },
            {
                "title": self.content,
                "ticket": self.ticket,
                "comments": self.get_email_comments(),
            },
            self.ticket.inbox.smtp_server if self.ticket.inbox.email_enabled else None,
            self.ticket.inbox.smtp_port if self.ticket.inbox.email_enabled else None,
            self.ticket.inbox.smtp_username if self.ticket.inbox.email_enabled else None,
            self.ticket.inbox.smtp_password if self.ticket.inbox.email_enabled else None,
            self.ticket.inbox.smtp_security if self.ticket.inbox.email_enabled else None
        )
