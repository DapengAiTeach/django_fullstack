from django.db import models
from django.conf import settings
from apps.content.models import Movie


class DownloadToken(models.Model):
    """
    下载令牌（短期有效）
    - 由系统生成
    - 用于允许某设备在有效期内下载
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    device_id = models.CharField(
        max_length=64,
        verbose_name="设备ID",
    )
    expires_at = models.DateTimeField(
        verbose_name="过期时间",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "download_token"
        verbose_name = "下载令牌"
        verbose_name_plural = "下载令牌"

    def __str__(self) -> str:
        return f"{self.user} - {self.movie} - {self.device_id}"


class DownloadDailyQuota(models.Model):
    """
    下载每日配额统计
    - 用于限制每日下载次数
    - unique_together 用于并发场景下保证唯一行
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    date = models.DateField(
        verbose_name="日期",
    )
    count = models.IntegerField(
        default=0,
        verbose_name="已使用次数",
    )

    class Meta:
        db_table = "download_daily_quota"
        verbose_name = "下载每日配额"
        verbose_name_plural = "下载每日配额"
        unique_together = ("user", "movie", "date")

    def __str__(self) -> str:
        return f"{self.user} - {self.movie} - {self.date}（{self.count}次）"
