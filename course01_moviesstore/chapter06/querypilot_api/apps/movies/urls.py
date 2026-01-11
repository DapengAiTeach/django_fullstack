from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.movies.views import MovieViewSet

app_name = "movies"

router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movie")

urlpatterns = [
    path("", include(router.urls)),
]