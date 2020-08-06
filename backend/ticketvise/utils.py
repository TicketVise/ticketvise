"""
Utils
-------------------------------
Various utility functions for use in python files.
"""
from base64 import b64encode
from io import BytesIO
from os import path

import numpy as np
from PIL import ImageColor, Image

from .models.ticket import Ticket
from .models.user import User
from .settings import DEFAULT_AVATAR_PATH, DEFAULT_INBOX_IMAGE_PATH


def edit_inbox_image_to_base64(image_path, color):
    """
    Edit the inbox image and encode it in base64.

    :param image_path: Path to the image
    :param color: Color to apply to the color filter

    :return: Base64-encoded image.
    """
    if not path.exists(f"ticketvise/{image_path}") or image_path == DEFAULT_INBOX_IMAGE_PATH:
        image = Image.open(f"ticketvise{DEFAULT_INBOX_IMAGE_PATH}")
    else:
        image = Image.open(f"ticketvise/{image_path}")

    image = apply_color_filter(image, color)
    image = crop_image(image)

    return convert_to_base64(image)


def apply_color_filter(image, color, alpha=0.6):
    """
    Apply a simple linear color filter to the image.

    :param image: Image to apply the color to
    :param color: Color to use in the filter
    :param alpha: Weight to give to the color

    :return: Color filterd image
    """
    inbox_array = np.array(image)
    inbox_array = inbox_array[:, :, :3]
    color_array = np.zeros_like(inbox_array)
    color_array[:, :] = hex_to_rgb(color)

    final_array = (1 - alpha) * color_array + alpha * inbox_array
    final_array = final_array.astype(np.int8)

    return Image.fromarray(final_array.astype(np.uint8))


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


def convert_to_base64(image):
    """
    Convert an image to base64.
    Source: https://stackoverflow.com/a/42505258

    :param image: Image to convert

    :return: Base64 string
    """
    in_mem_file = BytesIO()
    image.save(in_mem_file, format="PNG")
    in_mem_file.seek(0)
    image_bytes = in_mem_file.read()
    base64_encoded_result_bytes = b64encode(image_bytes)

    return base64_encoded_result_bytes.decode("ascii")


def _convert_to_linear(srgb):
    """
    Converts sRGB to linear RGB.
    Uses a modified version of https://en.wikipedia.org/wiki/SRGB#The_reverse_transformation.
    Translated from: https://github.com/jgthms/bulma/blob/master/sass/utilities/functions.sass.

    :param float srgb: RGB value to convert.

    :return: The linear value of the RGB color.
    :rtype: float
    """
    value = srgb / 255

    if value < 0.03928:
        value /= 12.92
    else:
        value = (value + 0.055) / 1.055
        value = pow(value, 2)

    return value


def hex_to_rgb(hex_color):
    """
    Convert hex color to RGB values.

    :param str hex_color: Hex color to convert.

    :return: RGB values from hex color.
    :rtype: tuple
    """
    return ImageColor.getcolor(hex_color, "RGB")


def _get_color_luminance(hex_color):
    """
    Get the relative color luminance of the color.
    Relative luminance multipliers: https://en.wikipedia.org/wiki/Relative_luminance.

    :param str hex_color: Hex color to get relative luminance of.

    :return: Relative luminance of color.
    :rtype: float
    """
    multipliers = (0.2126, 0.7152, 0.0722)

    return sum(
        map(lambda value, multiplier: _convert_to_linear(value) * multiplier, hex_to_rgb(hex_color), multipliers)
    )


def get_text_color(background_color):
    """
    Get the text color (black or white) depending on the background color.

    :param str background_color: Background color to get text color from.

    :return: Text color.
    :rtype: str
    """
    return "#000000" if _get_color_luminance(background_color) > 0.55 else "#ffffff"


def get_global_context():
    """
    Obtain the global context.

    :return: Global context template variables.
    :rtype: dict
    """
    return {
        "DEFAULT_AVATAR_PATH": DEFAULT_AVATAR_PATH,
        "ROLE_STUDENT": User.Roles.STUDENT,
        "ROLE_ASSISTANT": User.Roles.ASSISTANT,
        "ROLE_COORDINATOR": User.Roles.COORDINATOR,
        "STATUS_PENDING": Ticket.Status.PENDING,
        "STATUS_ASSIGNED": Ticket.Status.ASSIGNED,
        "STATUS_ANSWERED": Ticket.Status.ANSWERED,
        "STATUS_CLOSED": Ticket.Status.CLOSED,
    }


def add_global_context(context_dict):
    """
    Update the context dictionary.

    :param dict context_dict: The global context.

    :return: Context dictionary updated with global context.
    :rtype: dict
    """
    context_dict.update(get_global_context())


def limit(min_val, max_val, val):
    """
    Return the value clipped to the maximumum and minimum values specified.

    :param min: Minimum value.
    :type min: int or float
    :param max: Maximum value.
    :type max: int or float
    :param val: The value to clip.
    :type val: int or float

    :return: Clipped value.
    :rtype: int or float
    """
    return min(max_val, max(min_val, val))


def add_pagination_context(context, page, last_page):
    """
    Add the context variables to implement pagination.

    :param dict context: The context.
    :param int page: The number of the page.
    :param int last_page: The number of the last page.
    """
    context["next_page"] = page + 1
    context["previous_page"] = page - 1
    context["first_page"] = 0
    context["last_page"] = last_page
    context["page"] = page


def add_page_item_context(context, item, item_name, page, results_per_page):
    """
    Add the items to the context variable. Used for lists.

    :param dict context: The context.
    :param list item: The item.
    :param str item_name: The name of the item.
    :param int page: The number of the page.
    :param int results_per_page: The number of results shown on a page.
    """
    if len(item) > 0:
        context[item_name] = item[page * results_per_page:page * results_per_page + results_per_page]
    else:
        context[item_name] = []
