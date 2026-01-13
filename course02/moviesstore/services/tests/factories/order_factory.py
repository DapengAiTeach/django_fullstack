# services/tests/factories/order_factory.py
from __future__ import annotations

from typing import Iterable, List

from apps.orders.models import PurchaseOrder, PurchaseOrderItem
from services.domain.order_service import OrderItemCreateDTO, OrderService


def create_order(
    *,
    user,
    movies: Iterable,
    price_coin_map: dict | None = None,
    
) -> PurchaseOrder:
    """
    创建订单（测试工厂，不扣款、不授权）

    参数说明：
    - user: 下单用户
    - movies: 电影对象列表（Iterable[Movie]）
    - price_coin_map:
        - 可选，用于指定每个电影的价格
        - 例如 {movie1.id: 10, movie2.id: 20}
        - 不传则默认每个 movie.price_coin
    - remark: 订单备注（测试用）

    返回：
    - PurchaseOrder（状态：CREATED）
    """
    movies = list(movies)
    if not movies:
        raise ValueError("movies 不能为空")

    items: List[OrderItemCreateDTO] = []

    for movie in movies:
        if not getattr(movie, "id", None):
            raise ValueError("movie 必须是已保存对象")

        price = (
            price_coin_map.get(movie.id)
            if price_coin_map
            else getattr(movie, "price_coin", None)
        )
        if price is None:
            raise ValueError("无法确定 movie 的 price_coin")

        items.append(
            OrderItemCreateDTO(
                movie=movie,
                price_coin=price,
            )
        )

    order = OrderService.create_order(
        user=user,
        items=items,

    )
    return order


def create_single_movie_order(
    *,
    user,
    movie,
    price_coin: int | None = None,
) -> PurchaseOrder:
    """
    创建单电影订单（语义化快捷方法）
    """
    return create_order(
        user=user,
        movies=[movie],
        price_coin_map={movie.id: price_coin}
        if price_coin is not None
        else None,
    )


def create_multi_movie_order(
    *,
    user,
    movies: Iterable,
) -> PurchaseOrder:
    """
    创建多电影订单（用于测试批量购买 / 边界情况）
    """
    return create_order(
        user=user,
        movies=movies,
    )


def mark_order_completed(order: PurchaseOrder) -> PurchaseOrder:
    """
    将订单标记为已完成（测试辅助）

    ⚠️ 注意：
    - 这是“测试捷径”
    - 正常业务中应由 PurchaseFlow 更新状态
    """
    order.status = PurchaseOrder.Status.COMPLETED
    order.save(update_fields=["status"])
    return order


def get_order_items(order: PurchaseOrder):
    """
    获取订单明细列表（测试辅助）
    """
    return PurchaseOrderItem.objects.filter(order=order).select_related("movie")
