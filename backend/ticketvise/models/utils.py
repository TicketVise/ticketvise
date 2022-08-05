from django.db import models

class SchedulingAlgorithm(models.TextChoices):
    """
    Choices for the ``scheduling_algorithm`` field of :class:`Label` and
    :class:`Inbox`.
    """

    #: Schedules tickets in a round-robin fashion.
    ROUND_ROBIN = ("round-robin", "Round Robin")
    #: Assigns tickets to the assistant with the least assigned tickets.
    LEAST_ASSIGNED_FIRST = ("least-assigned-first", "Least Assigned First")
    # Schedule tickets based on sections
    SECTIONS = ("sections", "Workgroup")
    # Schedule all to one assistant
    FIXED = ("fixed", "Fixed")

class MailSecurity(models.TextChoices):
    NONE = ('NONE', 'None')
    STARTTLS = ('STARTTLS', 'STARTTLS')
    TLS = ('TLS', 'TLS')


class InboundMailProtocol(models.TextChoices):
    POP3 = 'POP3'
    IMAP = 'IMAP'
