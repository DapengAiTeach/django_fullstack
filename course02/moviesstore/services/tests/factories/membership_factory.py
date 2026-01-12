# services/tests/factories/membership_factory.py
from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.membership.models import Membership


def create_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    status: str = Membership.Status.ACTIVE,
    start_at=None,
    end_at=None,
) -> Membership:
    """
    创建会员记录（测试工厂，底层方法）

    参数：
    - user: 用户对象（必传）
    - plan: Membership.Plan.MONTH / YEAR
    - status: Membership.Status.ACTIVE / EXPIRED / GRACE
    - start_at / end_at: 可手动指定时间区间
    """
    now = timezone.now()

    if start_at is None:
        start_at = now

    if end_at is None:
        # 默认：一个月有效期
        end_at = start_at + timedelta(days=30)

    return Membership.objects.create(
        user=user,
        plan=plan,
        status=status,
        start_at=start_at,
        end_at=end_at,
    )


# =============================
# 语义化快捷方法（强烈推荐在测试中使用）
# =============================

def create_active_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    days: int = 30,
) -> Membership:
    """
    创建当前有效的会员
    """
    now = timezone.now()
    return create_membership(
        user=user,
        plan=plan,
        status=Membership.Status.ACTIVE,
        start_at=now - timedelta(days=1),
        end_at=now + timedelta(days=days),
    )


def create_expired_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    days_ago: int = 1,
) -> Membership:
    """
    创建已过期会员
    """
    now = timezone.now()
    return create_membership(
        user=user,
        plan=plan,
        status=Membership.Status.EXPIRED,
        start_at=now - timedelta(days=30 + days_ago),
        end_at=now - timedelta(days=days_ago),
    )


def create_grace_membership(
    *,
    user,
    plan: str = Membership.Plan.MONTH,
    grace_days: int = 3,
) -> Membership:
    """
    创建宽限期会员（例如：刚过期但仍允许访问）
    """
    now = timezone.now()
    return create_membership(
        user=user,
        plan=plan,
        status=Membership.Status.GRACE,
        start_at=now - timedelta(days=30),
        end_at=now - timedelta(days=1),
    )
