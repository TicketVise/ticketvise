"""
Utils
-------------------------------
Various utility functions for use in python files.
"""
import random

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

def random_preselected_color():
    """Randomly selected a color from a pre-defined list. The colors are the 500 colors from tailwind."""

    return random.choice([
        "#686F7D",
        "#6B7280",
        "#EC5050",
        "#F05252",
        "#FF5A1F",
        "#C27803",
        "#0E9F6E",
        "#0694A2",
        "#3F83F8",
        "#6875F5",
        "#9061F9"
    ])


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.page.paginator.count,
            "results": data,
            "page_number": self.page.number,
            "page_size": self.page_size,
            "total_pages": self.page.paginator.num_pages,
        })
