# services/tests/factories/download_factory.py
from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.download.models import DownloadToken, DownloadQuota


def create_download_token(
    *,
    user,
    movie,
    device_id: str = "test-device",
    expires_minutes: int = 10,
) -> DownloadToken:
    """
    创建下载 Token（测试工厂）

    参数：
    - user: 用户对象
    - movie: 电影对象
    - device_id: 设备标识
    - expires_minutes: 多少分钟后过期

    注意：
    - factory 不做任何权限判断
    - token 是否有效应由 DownloadService / DownloadFlow 测试
    """
    expires_at = timezone.now() + timedelta(minutes=expires_minutes)

    return DownloadToken.objects.create(
        user=user,
        movie=movie,
        device_id=device_id,
        expires_at=expires_at,
    )


def create_expired_download_token(
    *,
    user,
    movie,
    device_id: str = "test-device",
    expired_minutes_ago: int = 5,
) -> DownloadToken:
    """
    创建已过期的下载 Token（用于异常测试）
    """
    expires_at = timezone.now() - timedelta(minutes=expired_minutes_ago)

    return DownloadToken.objects.create(
        user=user,
        movie=movie,
        device_id=device_id,
        expires_at=expires_at,
    )


def create_download_quota(
    *,
    user,
    movie,
    date=None,
    count: int = 0,
) -> DownloadQuota:
    """
    创建下载配额记录（测试工厂）

    参数：
    - user: 用户对象
    - movie: 电影对象
    - date: 日期（默认今天）
    - count: 已下载次数
    """
    if date is None:
        date = timezone.localdate()

    return DownloadQuota.objects.create(
        user=user,
        movie=movie,
        date=date,
        count=count,
    )


def reset_download_data(
    *,
    user,
    movie=None,
):
    """
    重置下载相关数据（测试辅助）

    使用场景：
    - 多个测试共用同一 user/movie
    - 确保配额/token 干净

    参数：
    - user: 用户对象（必传）
    - movie: 电影对象（可选，不传则清空该用户所有下载数据）
    """
    token_qs = DownloadToken.objects.filter(user=user)
    quota_qs = DownloadQuota.objects.filter(user=user)

    if movie is not None:
        token_qs = token_qs.filter(movie=movie)
        quota_qs = quota_qs.filter(movie=movie)

    token_qs.delete()
    quota_qs.delete()
