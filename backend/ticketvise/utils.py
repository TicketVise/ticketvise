"""
Utils
-------------------------------
Various utility functions for use in python files.
"""

from PIL import ImageColor

from .models.ticket import Status
from .models.user import Role
from .settings import DEFAULT_AVATAR_PATH


def crop_image(image):
    """
    Crop the image to a 4:3 ratio.

    :param image: Image to crop

    :return: Cropped image
    """
    width, height = image.size
    expected_height = (width / 4) * 3
    expected_width = (height / 3) * 4

    # If the expected height is larger than the actual height, then we crop
    # the width of the image, otherwise we crop the height of the image.
    if height < expected_height:
        width_difference = width - expected_width
        crop_per_side = int(width_difference / 2)

        return image.crop((crop_per_side, 0, width - crop_per_side, height))
    else:
        height_difference = height - expected_height
        crop_per_side = int(height_difference / 2)

        return image.crop((0, crop_per_side, width, height - crop_per_side))


def get_text_color(background_color):
    """
    Get the text color (black or white) depending on the background color.

    :param str background_color: Background color to get text color from.

    :return: Text color.
    :rtype: str
    """
    r, g, b = ImageColor.getcolor(background_color, "RGB")
    return "#000000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#ffffff"


def get_global_context():
    """
    Obtain the global context.

    :return: Global context template variables.
    :rtype: dict
    """
    return {
        "DEFAULT_AVATAR_PATH": DEFAULT_AVATAR_PATH,
        "ROLE_STUDENT": Role.GUEST,
        "ROLE_ASSISTANT": Role.AGENT,
        "ROLE_COORDINATOR": Role.MANAGER,
        "STATUS_PENDING": Status.PENDING,
        "STATUS_ASSIGNED": Status.ASSIGNED,
        "STATUS_ANSWERED": Status.ANSWERED,
        "STATUS_CLOSED": Status.CLOSED,
    }


def add_global_context(context_dict):
    """
    Update the context dictionary.

    :param dict context_dict: The global context.

    :return: Context dictionary updated with global context.
    :rtype: dict
    """
    context_dict.update(get_global_context())
