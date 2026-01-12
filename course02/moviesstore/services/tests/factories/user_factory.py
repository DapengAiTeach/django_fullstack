# services/tests/factories/user_factory.py
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from django.contrib.auth import get_user_model


@dataclass(frozen=True)
class UserCreateDTO:
    """
    测试用用户创建参数对象

    说明：
    - factories 里用 DTO 是为了让测试更清晰、可读、可维护
    - 你也可以不使用 DTO，直接传参，但 DTO 更适合中大型项目长期维护
    """
    username: str
    password: str
    email: str
    is_staff: bool = False
    is_superuser: bool = False
    is_active: bool = True


def _unique_username(prefix: str = "u") -> str:
    """
    生成唯一用户名，避免测试并发/重复运行时冲突
    """
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _unique_email(prefix: str = "u") -> str:
    """
    生成唯一邮箱，避免唯一约束冲突
    """
    return f"{prefix}_{uuid.uuid4().hex[:10]}@example.com"


def build_user_dto(
    *,
    username: Optional[str] = None,
    password: str = "TestPassw0rd!",
    email: Optional[str] = None,
    is_staff: bool = False,
    is_superuser: bool = False,
    is_active: bool = True,
) -> UserCreateDTO:
    """
    构建用户 DTO（仅用于测试）
    """
    return UserCreateDTO(
        username=username or _unique_username(),
        password=password,
        email=email or _unique_email(),
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
    )


def create_user(
    *,
    username: Optional[str] = None,
    password: str = "TestPassw0rd!",
    email: Optional[str] = None,
    is_active: bool = True,
    **extra_fields,
):
    """
    创建普通用户（测试工厂）

    参数：
    - username/email 可不传，自动生成唯一值
    - password 默认可用
    - extra_fields 用于兼容自定义 User 模型的额外字段（如 phone/nickname 等）
    """
    User = get_user_model()
    dto = build_user_dto(
        username=username,
        password=password,
        email=email,
        is_active=is_active,
    )

    # create_user 会自动处理密码哈希
    user = User.objects.create_user(
        username=dto.username,
        email=dto.email,
        password=dto.password,
        **extra_fields,
    )

    # Django 默认 create_user 会让 is_active=True，这里按入参强制覆盖
    if hasattr(user, "is_active") and user.is_active != dto.is_active:
        user.is_active = dto.is_active
        user.save(update_fields=["is_active"])

    return user


def create_admin(
    *,
    username: Optional[str] = None,
    password: str = "AdminPassw0rd!",
    email: Optional[str] = None,
    is_active: bool = True,
    **extra_fields,
):
    """
    创建管理员用户（测试工厂）
    - 用于模拟后台管理端 operator
    """
    User = get_user_model()
    dto = build_user_dto(
        username=username or _unique_username("admin"),
        password=password,
        email=email or _unique_email("admin"),
        is_staff=True,
        is_superuser=True,
        is_active=is_active,
    )

    # create_superuser 会自动处理密码、is_staff、is_superuser
    user = User.objects.create_superuser(
        username=dto.username,
        email=dto.email,
        password=dto.password,
        **extra_fields,
    )

    # 强制状态一致
    updates = []
    if hasattr(user, "is_active") and user.is_active != dto.is_active:
        user.is_active = dto.is_active
        updates.append("is_active")

    if hasattr(user, "is_staff") and not user.is_staff:
        user.is_staff = True
        updates.append("is_staff")

    if hasattr(user, "is_superuser") and not user.is_superuser:
        user.is_superuser = True
        updates.append("is_superuser")

    if updates:
        user.save(update_fields=updates)

    return user
