# services/domain/user_service.py
from __future__ import annotations

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from services.common.exceptions import NotFound, BusinessRuleViolation


class UserService:
    """
    用户域 Service（后台管理 + App/Web 统一入口）

    职责边界：
    - 账号启用/禁用（后台运营常用）
    - 用户资料更新（可扩展）
    - 用户查询列表（后台）
    - 不处理登录（登录属于认证体系 / movie_auth）

    说明：
    - Django 默认 User 模型有 is_active 字段，用于控制账号是否可登录
    - 这里统一通过 Service 修改 is_active，避免散落在 View/脚本里
    """

    @staticmethod
    def _get_user_model():
        """
        延迟获取 User 模型，避免循环 import，并兼容自定义 AUTH_USER_MODEL
        """
        from django.contrib.auth import get_user_model
        return get_user_model()

    # =============================
    # 读：单个用户
    # =============================

    @staticmethod
    def get_user(*, user_id: int):
        """
        获取用户对象
        """
        User = UserService._get_user_model()
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise NotFound("用户不存在")
        return user

    @staticmethod
    def get_user_by_username(*, username: str):
        """
        按用户名查询用户（可用于后台检索）
        """
        if not username:
            raise BusinessRuleViolation("username 不能为空")

        User = UserService._get_user_model()
        user = User.objects.filter(username=username).first()
        if not user:
            raise NotFound("用户不存在")
        return user

    @staticmethod
    def get_user_by_email(*, email: str):
        """
        按邮箱查询用户（可用于后台检索）
        """
        if not email:
            raise BusinessRuleViolation("email 不能为空")

        User = UserService._get_user_model()
        user = User.objects.filter(email=email).first()
        if not user:
            raise NotFound("用户不存在")
        return user

    # =============================
    # 读：后台列表查询（CRUD）
    # =============================

    @staticmethod
    def list_users(
        *,
        keyword: str | None = None,
        is_active: bool | None = None,
        is_staff: bool | None = None,
        is_superuser: bool | None = None,
    ) -> QuerySet:
        """
        后台用户列表查询（返回 QuerySet，调用方自行分页）

        参数：
        - keyword：模糊搜索 username/email
        - is_active/is_staff/is_superuser：精确筛选
        """
        User = UserService._get_user_model()
        qs = User.objects.all()

        if is_active is not None:
            qs = qs.filter(is_active=is_active)

        if is_staff is not None:
            qs = qs.filter(is_staff=is_staff)

        if is_superuser is not None:
            qs = qs.filter(is_superuser=is_superuser)

        if keyword:
            qs = qs.filter(username__icontains=keyword) | qs.filter(email__icontains=keyword)

        # 尽量保证排序稳定
        return qs.order_by("-date_joined", "-id")

    # =============================
    # 写：启用/禁用（后台管理核心）
    # =============================

    @staticmethod
    @transaction.atomic
    def disable_user(*, user_id: int, operator=None, reason: str | None = None):
        """
        禁用用户账号（使其无法登录）
        """
        User = UserService._get_user_model()
        user = User.objects.select_for_update().filter(id=user_id).first()
        if not user:
            raise NotFound("用户不存在")

        if not user.is_active:
            return user

        user.is_active = False
        # 可选：若存在更新字段，写入更新时间
        if hasattr(user, "updated_at"):
            user.updated_at = timezone.now()

        user.save(update_fields=["is_active"] + (["updated_at"] if hasattr(user, "updated_at") else []))
        return user

    @staticmethod
    @transaction.atomic
    def enable_user(*, user_id: int, operator=None, reason: str | None = None):
        """
        启用用户账号（允许登录）
        """
        User = UserService._get_user_model()
        user = User.objects.select_for_update().filter(id=user_id).first()
        if not user:
            raise NotFound("用户不存在")

        if user.is_active:
            return user

        user.is_active = True
        if hasattr(user, "updated_at"):
            user.updated_at = timezone.now()

        user.save(update_fields=["is_active"] + (["updated_at"] if hasattr(user, "updated_at") else []))
        return user

    # =============================
    # 写：用户资料更新（可扩展）
    # =============================

    @staticmethod
    @transaction.atomic
    def update_profile(*, user_id: int, data: dict):
        """
        更新用户资料（基础实现）
        仅允许更新白名单字段，避免调用方随意写入敏感字段
        """
        allow_fields = {"first_name", "last_name", "email"}

        User = UserService._get_user_model()
        user = User.objects.select_for_update().filter(id=user_id).first()
        if not user:
            raise NotFound("用户不存在")

        for k, v in data.items():
            if k not in allow_fields:
                continue
            setattr(user, k, v)

        if hasattr(user, "updated_at"):
            user.updated_at = timezone.now()

        # 只更新允许字段
        update_fields = [k for k in data.keys() if k in allow_fields]
        if hasattr(user, "updated_at"):
            update_fields.append("updated_at")

        if update_fields:
            user.save(update_fields=update_fields)

        return user

    # =============================
    # 写：重置密码（后台运维常用）
    # =============================

    @staticmethod
    @transaction.atomic
    def reset_password(*, user_id: int, new_password: str):
        """
        后台重置用户密码（管理员能力）
        """
        if not new_password or len(new_password) < 8:
            raise BusinessRuleViolation("新密码长度至少 8 位")

        User = UserService._get_user_model()
        user = User.objects.select_for_update().filter(id=user_id).first()
        if not user:
            raise NotFound("用户不存在")

        user.set_password(new_password)
        if hasattr(user, "updated_at"):
            user.updated_at = timezone.now()
            user.save(update_fields=["password", "updated_at"])
        else:
            user.save(update_fields=["password"])

        return user
