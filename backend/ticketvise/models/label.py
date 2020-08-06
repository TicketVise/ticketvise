"""
Label
-------------------------------
Contains all entity sets for the label database.

**Table of contents**
* :class:`Label`
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from ticketvise.models.validators import validate_hex_color


class Label(models.Model):
    """
    This model represents a label. A label can be part of a single :class:`Inbox` and can be
    applied to multiple :class:`Ticket` s. The labels of a ticket are then used to schedule it.

    :reverse relations: * **tickets** -- Set of :class:`Ticket` s that the label has been applied to.
    """

    #: The :class:`Inbox` that the label is registered in.
    inbox = models.ForeignKey("ticketvise.Inbox", on_delete=models.CASCADE, related_name="labels")
    #: Label color, must be a valid hex color.
    color = models.CharField(max_length=7, validators=[validate_hex_color], default="#ff0000")
    #: Label name.
    name = models.CharField(max_length=50, default="")
    #: If ``True``, the label is visible for students when creating a ticket. Defaults to ``False``.
    is_form_label = models.BooleanField(default=False)
    #: Indicates if the instance is active or not. Defaults to ``True``.
    is_active = models.BooleanField(_("Is active"), default=True)

    def __str__(self):
        return self.name
