"""
Label
-------------------------------
Contains all entity sets for the label database.

**Table of contents**
* :class:`Label`
"""
from django.db import models

from ticketvise.models.validators import validate_hex_color
from ticketvise.utils import random_color


class Label(models.Model):
    """
    This model represents a label. A label can be part of a single :class:`Inbox` and can be
    applied to multiple :class:`Ticket` s. The labels of a ticket are then used to schedule it.

    :reverse relations: * **tickets** -- Set of :class:`Ticket` s that the label has been applied to.
    """

    inbox = models.ForeignKey("Inbox", on_delete=models.CASCADE, related_name="labels")
    color = models.CharField(max_length=7, validators=[validate_hex_color], default=random_color)
    name = models.CharField(max_length=50, default="")
    is_visible_to_guest = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_edited = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
