"""
Utils
-------------------------------
Various utility functions for use in python files.
"""
import random

from PIL import ImageColor


def random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


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
    return "#374151" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#ffffff"

