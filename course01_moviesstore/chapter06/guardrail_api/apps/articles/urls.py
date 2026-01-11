from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.articles.views import ArticleViewSet

app_name = "articles"

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
]