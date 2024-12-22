from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from rest_framework.response import Response


class GlobalPagination(PageNumberPagination):
    # Fetch the page size from settings
    page_size = getattr(settings, "PAGINATION_PAGE_SIZE", 10)
    page_size_query_param = (
        "page_size"  # Allow users to customize page size in requests
    )
    max_page_size = 100  # Optional: Set a limit for maximum page size

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "current_page": self.page.number,
                "page_size": self.page_size,
                "results": data,
            }
        )
