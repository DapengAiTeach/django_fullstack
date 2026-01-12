# services/domain/download_service.py
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from apps.download.models import DownloadToken, DownloadQuota
from services.common.exceptions import (
    PermissionDenied,
    BusinessRuleViolation,
    NotFound,
)


class DownloadService:
    """
    下载域 Service（CRUD + 风控基础能力）

    职责：
    - 创建下载 Token
    - 校验下载 Token
    - 管理每日下载配额（计数）
    - 为 Core Flow 提供基础能力
    """

    DEFAULT_TOKEN_EXPIRE_MINUTES = 10

    # =============================
    # 下载 Token 相关
    # =============================

    @staticmethod
    def create_token(
        *,
        user,
        movie,
        device_id: str,
        expires_at=None,
    ) -> DownloadToken:
        """
        创建下载 Token

        注意：
        - 权限校验（是否拥有电影）必须在上层 Flow 中完成
        - 这里只负责 Token 的创建与存储
        """

        if not device_id:
            raise BusinessRuleViolation("device_id 不能为空")

        if expires_at is None:
            expires_at = timezone.now() + timedelta(
                minutes=DownloadService.DEFAULT_TOKEN_EXPIRE_MINUTES
            )

        return DownloadToken.objects.create(
            user=user,
            movie=movie,
            device_id=device_id,
            expires_at=expires_at,
        )

    @staticmethod
    def verify_token(token: str, device_id: str) -> DownloadToken:
        """
        校验下载 Token 是否有效

        校验规则：
        - Token 存在
        - 未过期
        - device_id 一致
        """

        download_token = (
            DownloadToken.objects.select_related("user", "movie")
            .filter(token=token)
            .first()
        )

        if not download_token:
            raise PermissionDenied("无效的下载凭证")

        if download_token.expires_at < timezone.now():
            raise PermissionDenied("下载凭证已过期")

        if download_token.device_id != device_id:
            raise PermissionDenied("设备不匹配")

        return download_token

    # =============================
    # 下载配额（风控）
    # =============================

    @staticmethod
    @transaction.atomic
    def increase_daily_quota(*, user, movie, date=None) -> DownloadQuota:
        """
        增加用户某天的下载次数（并发安全）

        - 使用行级锁防止并发超限
        - 必须在真正开始下载前调用
        """

        if date is None:
            date = timezone.localdate()

        quota, created = (
            DownloadQuota.objects.select_for_update()
            .get_or_create(
                user=user,
                movie=movie,
                date=date,
                defaults={"count": 0},
            )
        )

        quota.count += 1
        quota.save(update_fields=["count"])

        return quota

    @staticmethod
    def can_download(
        *,
        user,
        movie,
        daily_limit: int,
        date=None,
    ) -> bool:
        """
        判断用户当天是否还能下载（只读）

        - 不加锁
        - 不修改数据
        """

        if date is None:
            date = timezone.localdate()

        quota = DownloadQuota.objects.filter(
            user=user,
            movie=movie,
            date=date,
        ).first()

        if not quota:
            return True

        return quota.count < daily_limit

    # =============================
    # 后台 / 运维查询能力（CRUD）
    # =============================

    @staticmethod
    def get_quota(
        *,
        user,
        movie,
        date,
    ) -> DownloadQuota | None:
        """
        查询指定用户、电影、日期的下载配额
        """
        return DownloadQuota.objects.filter(
            user=user,
            movie=movie,
            date=date,
        ).first()

    @staticmethod
    def list_tokens(
        *,
        user=None,
        movie=None,
        is_active: bool | None = None,
    ):
        """
        后台查询下载 Token 列表

        参数：
        - user: 可选
        - movie: 可选
        - is_active:
            - True：仅未过期
            - False：仅已过期
            - None：全部
        """

        qs = DownloadToken.objects.all().select_related("user", "movie")

        if user:
            qs = qs.filter(user=user)

        if movie:
            qs = qs.filter(movie=movie)

        if is_active is True:
            qs = qs.filter(expires_at__gte=timezone.now())
        elif is_active is False:
            qs = qs.filter(expires_at__lt=timezone.now())

        return qs.order_by("-created_at")
