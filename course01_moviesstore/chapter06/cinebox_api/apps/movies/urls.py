from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.movies.views import MovieViewSet

app_name = "movies"

router = DefaultRouter()
# movies 这个名字就是 Resource（资源名）
router.register(r"movies", MovieViewSet, basename="movie")

urlpatterns = [
    path("", include(router.urls)),
]