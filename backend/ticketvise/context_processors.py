"""
Context processors
-------------------------------
Functions in this module can be used to add variables to the template context
of all templates.
"""
from .utils import get_global_context


def global_context(request):
    """
    Returns the global context variables for use in all templates.

    :param HTTPRequest request: Request content.

    :return: The global context variables.
    :rtype: dict
    """
    return get_global_context()
