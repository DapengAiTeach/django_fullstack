from rest_framework.viewsets import ModelViewSet

from apps.common.mixins import ApiResponseMixin
from apps.catalog.models import Product
from apps.catalog.serializers import ProductSerializer, ProductDetailSerializer


class ProductViewSet(ApiResponseMixin, ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        """
        同一资源不同场景用不同 Serializer：
        - list/create/update：ProductSerializer
        - retrieve（详情）：ProductDetailSerializer（包含嵌套与自定义字段）
        """
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer