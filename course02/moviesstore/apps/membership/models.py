from django.db import models
from django.conf import settings


class Membership(models.Model):
    """
    用户会员表
    """

    class Plan(models.TextChoices):
        MONTH = "MONTH", "月卡"
        YEAR = "YEAR", "年卡"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "生效中"
        GRACE = "GRACE", "宽限期"
        EXPIRED = "EXPIRED", "已过期"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    plan = models.CharField(
        max_length=20,
        choices=Plan.choices,
        verbose_name="会员类型",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="会员状态",
    )

    start_at = models.DateTimeField(
        verbose_name="开始时间",
    )
    end_at = models.DateTimeField(
        verbose_name="结束时间",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "membership"
        verbose_name = "会员"
        verbose_name_plural = "会员"

    def __str__(self) -> str:
        return f"{self.user} - {self.plan} - {self.status}"