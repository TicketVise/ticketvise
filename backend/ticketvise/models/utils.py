from django.db import models

class MailSecurity(models.TextChoices):
    NONE = ('NONE', 'None')
    STARTTLS = ('STARTTLS', 'STARTTLS')
    TLS = ('TLS', 'TLS')


class InboundMailProtocol(models.TextChoices):
    POP3 = 'POP3'
    IMAP = 'IMAP'