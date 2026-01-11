from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    对象级权限：
    - 作者本人可操作
    - 管理员可操作
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and (obj.author_id == request.user.id or request.user.is_staff))


class IsPublisherOrAdmin(BasePermission):
    """
    对象级权限：
    - 发布/取消发布：作者或管理员
    """

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and (obj.author_id == request.user.id or request.user.is_staff))


class IsNotLockedOrAdmin(BasePermission):
    """
    对象级权限：
    - 被锁定的文章禁止普通用户修改/删除
    - 管理员不受限制
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return not obj.is_locked