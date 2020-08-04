"""
Validators
-------------------------------
Contains all entity sets for the validators for the database.

**Table of contents**
* :class:`SchedulingAlgorithms`
* :class:`SchedulingParameters`
"""
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_hex_color(value):
    """
    Checks if the value is a valid hex color representation.
    If it is not, raises :exc:`django.core.exceptions.ValidationError`.

    :param str value: Hex color to validate.

    :raises ValidationError: If the hex color is not valid.
    """
    value = value.lower()
    pattern = r"#[0-9a-f]{6}"
    result = re.fullmatch(pattern, value)

    if result is None:
        raise ValidationError(_("%(value)s is not a valid hex color."), params={"value": value})
