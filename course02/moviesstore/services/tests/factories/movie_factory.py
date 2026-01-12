# services/tests/factories/movie_factory.py
from __future__ import annotations

import uuid
from typing import Optional

from apps.movies.models import Movie


def _unique_title(prefix: str = "测试电影") -> str:
    """
    生成唯一电影标题，避免测试中唯一约束冲突
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def create_movie(
    *,
    title: Optional[str] = None,
    price_coin: int = 10,
    status: str | None = None,
    year: int = 2025,
    is_active: bool = True,
    **extra_fields,
) -> Movie:
    """
    创建电影（测试工厂）

    设计目标：
    - 创建一条“合法、可购买”的电影记录
    - 默认状态：可售 / 上架
    - 供订单 / 授权 / 下载测试使用

    参数说明：
    - title: 电影标题（不传则自动生成唯一值）
    - price_coin: 电影金币价格
    - status: 电影状态（不传则使用模型默认）
    - year: 上映年份
    - is_active: 是否有效（软删除/上下架场景）
    - extra_fields: 兼容模型未来扩展字段
    """
    if price_coin <= 0:
        raise ValueError("price_coin 必须大于 0")

    data = {
        "title": title or _unique_title(),
        "price_coin": price_coin,
        "year": year,
        "is_active": is_active,
    }

    if status is not None:
        data["status"] = status

    data.update(extra_fields)

    movie = Movie.objects.create(**data)
    return movie


def create_onsale_movie(
    *,
    title: Optional[str] = None,
    price_coin: int = 10,
    **extra_fields,
) -> Movie:
    """
    创建“已上架/可售”的电影（语义化快捷方法）
    """
    return create_movie(
        title=title,
        price_coin=price_coin,
        status=Movie.Status.ONSALE,
        **extra_fields,
    )


def create_offline_movie(
    *,
    title: Optional[str] = None,
    price_coin: int = 10,
    **extra_fields,
) -> Movie:
    """
    创建“下架”的电影（用于异常/边界测试）
    """
    return create_movie(
        title=title,
        price_coin=price_coin,
        status=Movie.Status.OFFLINE,
        **extra_fields,
    )
