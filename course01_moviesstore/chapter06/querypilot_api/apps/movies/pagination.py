from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 50
    page_query_param = "page"

    def get_paginated_response(self, data):
        return Response({
            "results": data,
            "pagination": {
                "mode": "page",
                "page": self.page.number,
                "page_size": self.get_page_size(self.request),
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            }
        })


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 50

    def get_paginated_response(self, data):
        return Response({
            "results": data,
            "pagination": {
                "mode": "limit",
                "limit": self.get_limit(self.request),
                "offset": self.get_offset(self.request),
                "count": self.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            }
        })


class StandardCursorPagination(CursorPagination):
    page_size = 5
    page_size_query_param = "page_size"
    ordering = "-created_at"

    def get_paginated_response(self, data):
        return Response({
            "results": data,
            "pagination": {
                "mode": "cursor",
                "page_size": self.get_page_size(self.request),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            }
        })