from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from apps.common.mixins import ApiResponseMixin
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer


class HealthCheckAPIView(ApiResponseMixin, APIView):
    """
    APIView：最基础的 DRF 视图
    - 手写 get/post 等方法
    - 明确理解 Request / Response
    """

    def get(self, request):
        """
        request: DRF Request（封装了 Django request）
        - request.query_params：获取查询参数（?a=1）
        - request.data：获取 body（POST/PUT/PATCH 的 JSON）
        """
        payload = {
            "service": "bookpulse_api",
            "status": "running",
        }
        return Response(payload, status=status.HTTP_200_OK)


class ReviewListGenericAPIView(ApiResponseMixin, ListModelMixin, GenericAPIView):
    """
    GenericAPIView：解决 APIView 的重复劳动
    - 提供 queryset/serializer_class/lookup_field 等通用能力
    - Mixins 提供常用动作：List/Create/Retrieve/Update/Destroy
    这里我们只演示 ListModelMixin（列表）
    """
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        # ListModelMixin.list 会返回 Response(serializer.data)
        return self.list(request, *args, **kwargs)


class ReviewViewSet(ApiResponseMixin, ModelViewSet):
    """
    ModelViewSet：企业主线写法（最常用）
    - 自带 CRUD action
    - Router 自动生成路由
    """
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer