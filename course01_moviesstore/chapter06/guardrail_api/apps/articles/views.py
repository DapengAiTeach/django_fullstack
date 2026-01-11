from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions

from apps.common.mixins import ApiResponseMixin
from apps.articles.models import Article
from apps.articles.serializers import ArticleSerializer
from apps.articles.permissions import IsOwnerOrAdmin, IsPublisherOrAdmin, IsNotLockedOrAdmin


class ArticleViewSet(ApiResponseMixin, ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """
        关键点：
        - list：普通用户只看到自己的文章（业务需求）
        - retrieve/update/delete/action：必须允许 queryset 包含所有对象，
          否则会在 get_object 阶段直接 404，导致对象级权限无法触发（测试会失败）
        """
        qs = Article.objects.all().order_by("-created_at")

        if self.request.user.is_staff:
            return qs

        if self.action == "list":
            return qs.filter(author=self.request.user)

        # 非 list 场景返回全量，让对象级权限来决定是否允许访问
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ("lock", "unlock"):
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated(), DjangoModelPermissions()]

    def check_object_permissions(self, request, obj):
        """
        对象级权限组合：
        - 作者或管理员（IsOwnerOrAdmin）
        - 普通用户对锁定对象无权限（IsNotLockedOrAdmin）
        """
        super().check_object_permissions(request, obj)

        if not IsOwnerOrAdmin().has_object_permission(request, self, obj):
            self.permission_denied(request, message="not_owner")

        if not IsNotLockedOrAdmin().has_object_permission(request, self, obj):
            self.permission_denied(request, message="locked")

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        obj = self.get_object()

        if not IsPublisherOrAdmin().has_object_permission(request, self, obj):
            self.permission_denied(request, message="not_allowed_to_publish")

        obj.is_published = True
        obj.save(update_fields=["is_published"])
        return Response({"id": obj.id, "is_published": obj.is_published}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unpublish(self, request, pk=None):
        obj = self.get_object()

        if not IsPublisherOrAdmin().has_object_permission(request, self, obj):
            self.permission_denied(request, message="not_allowed_to_unpublish")

        obj.is_published = False
        obj.save(update_fields=["is_published"])
        return Response({"id": obj.id, "is_published": obj.is_published}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def lock(self, request, pk=None):
        obj = self.get_object()
        obj.is_locked = True
        obj.save(update_fields=["is_locked"])
        return Response({"id": obj.id, "is_locked": obj.is_locked}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def unlock(self, request, pk=None):
        obj = self.get_object()
        obj.is_locked = False
        obj.save(update_fields=["is_locked"])
        return Response({"id": obj.id, "is_locked": obj.is_locked}, status=status.HTTP_200_OK)
