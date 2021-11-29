import uuid
from django.db import models
from model_utils.managers import InheritanceManager

from ticketvise import settings
from ticketvise.mail.send import send_mail_template


class Notification(models.Model):
    objects = InheritanceManager()
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notifications")
    is_read = models.BooleanField(default=False)
    email_message_id = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
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

    def send_mail(self):
        send_mail_template(
            self.get_email_subject(),
            self.ticket.inbox.smtp_username if self.ticket.inbox.email_enabled else settings.DEFAULT_FROM_EMAIL,
            self.receiver.email,
            "comments",
            {
                "Message-Id": f"<{self.email_message_id}@{settings.DOMAIN}>".lower(),
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
            self.ticket.inbox.smtp_security if self.ticket.inbox.email_enabled else None,
            self.ticket.inbox.smtp_use_oauth2 if self.ticket.inbox.smtp_use_oauth2 else None
        )
