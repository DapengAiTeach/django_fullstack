from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from apps.common.mixins import ApiResponseMixin
from apps.movies.models import Movie
from apps.movies.serializers import MovieSerializer
from apps.movies.pagination import (
    StandardPageNumberPagination,
    StandardLimitOffsetPagination,
    StandardCursorPagination,
)


class MovieViewSet(ApiResponseMixin, ModelViewSet):
    queryset = Movie.objects.all().order_by("-created_at")
    serializer_class = MovieSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # filterset_fields 支持 lookup：rating__gte/rating__lte
    filterset_fields = {
        "genre": ["exact"],
        "year": ["exact", "gte", "lte"],
        "is_hot": ["exact"],
        "rating": ["exact", "gte", "lte"],
    }

    search_fields = ["title"]
    ordering_fields = ["year", "rating", "created_at"]
    ordering = ["-created_at"]

    def get_pagination_class(self):
        """
        通过查询参数 p 切换分页策略：
        - p=page   -> PageNumberPagination
        - p=limit  -> LimitOffsetPagination
        - p=cursor -> CursorPagination
        - 默认 page
        """
        mode = (self.request.query_params.get("p") or "page").lower()
        if mode == "limit":
            return StandardLimitOffsetPagination
        if mode == "cursor":
            return StandardCursorPagination
        return StandardPageNumberPagination

    def paginate_queryset(self, queryset):
        self.pagination_class = self.get_pagination_class()
        return super().paginate_queryset(queryset)