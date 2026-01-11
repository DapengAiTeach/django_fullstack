from rest_framework.viewsets import ModelViewSet
from apps.movies.models import Movie
from apps.movies.serializers import MovieSerializer
from apps.common.mixins import ApiResponseMixin


class MovieViewSet(ApiResponseMixin, ModelViewSet):
    """
    ViewSet = 一组 Endpoint 的集合（企业非常常用）

    Resource: movies
    Endpoints:
    - GET    /api/movies/        list
    - POST   /api/movies/        create
    - GET    /api/movies/{id}/   retrieve
    - PUT    /api/movies/{id}/   update
    - PATCH  /api/movies/{id}/   partial_update
    - DELETE /api/movies/{id}/   destroy
    """
    queryset = Movie.objects.all().order_by("-created_at")
    serializer_class = MovieSerializer
