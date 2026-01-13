# services/domain/order_service.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from apps.orders.models import PurchaseOrder, PurchaseOrderItem
from services.common.exceptions import NotFound, BusinessRuleViolation


@dataclass(frozen=True)
class OrderItemCreateDTO:
    """
    创建订单条目的输入对象（Service 入参标准化）
    """
    movie: object  # 这里不强绑定 apps.content.models.Movie，避免循环 import
    price_coin: int


class OrderService:
    """
    订单域 Service（CRUD + 状态流转 + 后台查询）

    职责边界：
    - 提供订单与订单明细的创建/查询/状态变更能力
    - 不负责扣款/发放授权（这些属于 core/purchase_flow.py 的闭环职责）
    - 为后台管理系统与 App/Web 端提供统一订单能力

    说明：
    - 订单是交易事实记录
    - 扣款与授权必须由“闭环 Flow”调用 WalletService/LicenseService 后再更新订单状态
    """

    # =============================
    # 写：创建订单（不扣款、不授权）
    # =============================

    @staticmethod
    @transaction.atomic
    def create_order(
        *,
        user,
        items: Iterable[OrderItemCreateDTO],
        remark: str | None = None,
    ) -> PurchaseOrder:
        """
        创建订单（仅落库订单与订单明细，不做扣款与授权）

        适用：
        - App/Web 下单准备阶段
        - 管理后台代客下单（后续由闭环 Flow 扣款/授权）

        约束：
        - items 不能为空
        - price_coin 必须为正整数
        - 同一订单内 movie 不允许重复（防止重复购买条目）
        """
        item_list = list(items)
        if not item_list:
            raise BusinessRuleViolation("订单明细不能为空")

        movie_ids = []
        total_coin = 0

        for it in item_list:
            if it.price_coin is None or it.price_coin <= 0:
                raise BusinessRuleViolation("订单明细价格必须大于 0")
            # movie 需要有 id 属性
            if not getattr(it.movie, "id", None):
                raise BusinessRuleViolation("订单明细电影无效")
            movie_ids.append(it.movie.id)
            total_coin += int(it.price_coin)

        if len(set(movie_ids)) != len(movie_ids):
            raise BusinessRuleViolation("同一订单内不允许重复购买同一电影")

        order = PurchaseOrder.objects.create(
            user=user,
            total_coin=total_coin,
            status=PurchaseOrder.Status.CREATED,
        )

        PurchaseOrderItem.objects.bulk_create(
            [
                PurchaseOrderItem(
                    order=order,
                    movie=it.movie,
                    price_coin=it.price_coin,
                )
                for it in item_list
            ]
        )

        return order

    # =============================
    # 读：订单查询（通用）
    # =============================

    @staticmethod
    def get_order(*, order_id: int) -> PurchaseOrder:
        """
        获取订单详情（含 user）
        """
        order = (
            PurchaseOrder.objects.select_related("user")
            .filter(id=order_id)
            .first()
        )
        if not order:
            raise NotFound("订单不存在")
        return order

    @staticmethod
    def get_order_with_items(*, order_id: int) -> PurchaseOrder:
        """
        获取订单并预加载 items（含 movie）
        """
        order = OrderService.get_order(order_id=order_id)
        # 预热 items
        _ = list(
            PurchaseOrderItem.objects.select_related("movie")
            .filter(order=order)
        )
        return order

    @staticmethod
    def list_orders(
        *,
        user=None,
        status: Optional[str] = None,
        created_from=None,
        created_to=None,
    ) -> QuerySet:
        """
        订单列表查询（返回 QuerySet，调用方自行分页）
        - 适用于后台管理系统与用户订单列表

        参数：
        - user：筛选某用户订单（可选）
        - status：筛选状态（可选）
        - created_from/created_to：按创建时间范围筛选（可选）
        """
        qs = PurchaseOrder.objects.all().select_related("user")

        if user is not None:
            qs = qs.filter(user=user)

        if status:
            qs = qs.filter(status=status)

        if created_from:
            qs = qs.filter(created_at__gte=created_from)

        if created_to:
            qs = qs.filter(created_at__lte=created_to)

        return qs.order_by("-created_at")

    @staticmethod
    def list_order_items(*, order: PurchaseOrder) -> QuerySet:
        """
        获取订单明细列表（返回 QuerySet）
        """
        return (
            PurchaseOrderItem.objects.select_related("movie")
            .filter(order=order)
            .order_by("id")
        )

    # =============================
    # 写：订单状态流转（不做扣款/授权）
    # =============================

    @staticmethod
    @transaction.atomic
    def set_status(*, order_id: int, status: str) -> PurchaseOrder:
        """
        强制设置订单状态（后台管理/补偿场景）
        调用方必须自行保证权限与审计。

        注意：
        - 正常交易流程请在 core/purchase_flow.py 内更新订单状态
        """
        order = PurchaseOrder.objects.select_for_update().filter(id=order_id).first()
        if not order:
            raise NotFound("订单不存在")

        # 仅做基础合法性校验（具体状态机可在此扩展）
        valid_status = {c for c, _ in PurchaseOrder.Status.choices}
        if status not in valid_status:
            raise BusinessRuleViolation("非法订单状态")

        order.status = status
        order.updated_at = timezone.now()
        order.save(update_fields=["status", "updated_at"])
        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(*, order_id: int, reason: str | None = None) -> PurchaseOrder:
        """
        取消订单（仅改变状态，不做退款/回滚授权）
        - 适用于未支付/未完成的订单取消

        若你未来支持“取消后退款/回收授权”，应在 core/ 里做闭环。
        """
        order = PurchaseOrder.objects.select_for_update().filter(id=order_id).first()
        if not order:
            raise NotFound("订单不存在")

        # 仅允许取消“未完成”的订单（可按你的状态机调整）
        if order.status in (PurchaseOrder.Status.COMPLETED,):
            raise BusinessRuleViolation("已完成订单不允许取消")

        order.status = PurchaseOrder.Status.CANCELED
        if hasattr(order, "remark"):
            extra = f"取消原因：{reason}" if reason else "取消订单"
            order.remark = (order.remark or "").strip()
            order.remark = (order.remark + "\n" + extra).strip()

        order.updated_at = timezone.now()
        order.save(update_fields=["status", "updated_at", "remark"] if hasattr(order, "remark") else ["status", "updated_at"])
        return order

    # =============================
    # 后台能力：订单重算总价（可选）
    # =============================

    @staticmethod
    @transaction.atomic
    def recalc_total_coin(*, order_id: int) -> PurchaseOrder:
        """
        重算订单总金币（后台纠错/导入数据修复场景）
        """
        order = PurchaseOrder.objects.select_for_update().filter(id=order_id).first()
        if not order:
            raise NotFound("订单不存在")

        items = PurchaseOrderItem.objects.filter(order=order)
        total = sum(int(i.price_coin) for i in items)

        order.total_coin = total
        order.updated_at = timezone.now()
        order.save(update_fields=["total_coin", "updated_at"])
        return order
