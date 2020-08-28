from django.db import models
from django.urls import reverse
from model_utils.managers import InheritanceManager

from ticketvise import settings
from ticketvise.email import send_mail_template


class Notification(models.Model):
    objects = InheritanceManager()
    receiver = models.ForeignKey("User", on_delete=models.CASCADE, related_name="notifications")
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



    def send_mail(self):
        send_mail_template(
            self.get_email_subject(),
            self.receiver.email,
            "comments",
            {
                # "Message-Id": f"<{self.ticket.comment_message_id}@{settings.DOMAIN}>",
            },
            {
                "title": self.content,
                "ticket": self.ticket,
                "comments": self.get_email_comments(),
                "url": f"https://{settings.DOMAIN}{reverse('ticket', self.ticket.inbox.id. self.ticket.ticket_inbox_id)}"
            }
        )
