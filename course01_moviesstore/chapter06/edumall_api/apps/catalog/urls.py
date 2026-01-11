from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.catalog.views import ProductViewSet
from apps.reviews.views import ProductReviewView

app_name = "catalog"

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    # Product 主资源（Router 自动生成 /products/ 与 /products/{id}/）
    path("", include(router.urls)),

    # Review 嵌套路由（不建议强塞 Router，手写更清晰）
    path("products/<int:product_id>/reviews/", ProductReviewView.as_view(), name="product-reviews"),
]