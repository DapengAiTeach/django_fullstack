# services/tests/factories/license_factory.py
from __future__ import annotations

from typing import Optional

from apps.orders.models import PurchaseLicense
from services.domain.license_service import LicenseService


def create_purchase_license(
    *,
    user,
    movie,
    order_item=None,
) -> PurchaseLicense:
    """
    创建用户购买电影的授权记录（测试工厂）

    参数：
    - user: 关联的用户对象
    - movie: 关联的电影对象
    - order_item: 关联的订单条目（如果有）

    返回：
    - 创建的 PurchaseLicense 对象
    """
    # 如果没有提供 order_item，模拟通过订单购买产生授权
    if not order_item:
        from services.tests.factories.order_factory import create_order
        order = create_order(user=user, movies=[movie])
        order_item = order.items.first()

    return LicenseService.grant_purchase_license(
        user=user,
        movie=movie,
        order_item=order_item,
    )


def create_force_license(
    *,
    user,
    movie,
    operator=None,
    remark=None,
) -> PurchaseLicense:
    """
    创建强制发放的授权记录（用于补偿/特殊场景）
    - 强制授权不需要订单项，可以通过虚拟订单或其他方式处理

    参数：
    - user: 关联的用户对象
    - movie: 关联的电影对象
    - operator: 操作员（可选，默认为 None）
    - remark: 备注信息（可选）

    返回：
    - 创建的 PurchaseLicense 对象
    """
    return LicenseService.grant_license_force(
        user=user,
        movie=movie,
        operator=operator,
        remark=remark,
    )
