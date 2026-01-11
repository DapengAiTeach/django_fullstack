from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.reviews.views import ReviewViewSet, HealthCheckAPIView, ReviewListGenericAPIView

app_name = "reviews"

router = DefaultRouter()
router.register(r"reviews", ReviewViewSet, basename="review")

urlpatterns = [
    # APIView 示例：健康检查
    path("health/", HealthCheckAPIView.as_view(), name="health"),

    # GenericAPIView 示例：演示用途（列表）
    path("reviews-generic/", ReviewListGenericAPIView.as_view(), name="reviews-generic"),

    # ViewSet + Router：企业主线
    path("", include(router.urls)),
]