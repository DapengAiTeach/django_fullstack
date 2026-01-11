from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.common.mixins import ApiResponseMixin
from apps.catalog.models import Product
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewWriteSerializer, ReviewReadSerializer


class ProductReviewView(ApiResponseMixin, APIView):
    """
    嵌套路由：
    - GET  /api/products/{product_id}/reviews/  列表
    - POST /api/products/{product_id}/reviews/  创建
    """

    def get_product(self, product_id: int) -> Product:
        return Product.objects.get(pk=product_id)

    def get(self, request, product_id: int):
        product = self.get_product(product_id)
        qs = product.reviews.all().order_by("-created_at")
        data = ReviewReadSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, product_id: int):
        product = self.get_product(product_id)

        # Serializer 使用 context 注入依赖（product）
        serializer = ReviewWriteSerializer(data=request.data, context={"product": product})
        serializer.is_valid(raise_exception=True)

        review = serializer.save()
        # 输出使用只读 serializer，避免 write_only 字段参与输出
        out = ReviewReadSerializer(review).data
        return Response(out, status=status.HTTP_201_CREATED)