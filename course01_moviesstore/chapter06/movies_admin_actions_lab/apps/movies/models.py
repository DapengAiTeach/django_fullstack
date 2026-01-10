from django.conf import settings
from django.db import models

class Movie(models.Model):
    STATUS_CHOICES = (
        (1, "草稿"),
        (2, "待上架"),
        (3, "已上架"),
        (4, "已下架"),
    )

    title = models.CharField("电影名", max_length=120)
    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=19.90)
    status = models.IntegerField("状态", choices=STATUS_CHOICES, default=1)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self):
        return self.title


class ActionLog(models.Model):
    """
    Action 日志：用于可追溯性
    """
    action = models.CharField("动作", max_length=100)
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="操作人",
        on_delete=models.SET_NULL,
        null=True,
    )
    target_ids = models.TextField("影响对象ID")
    remark = models.TextField("备注", blank=True)
    created_at = models.DateTimeField("时间", auto_now_add=True)

    class Meta:
        verbose_name = "Action日志"
        verbose_name_plural = "Action日志"

    def __str__(self):
        return f"{self.action} by {self.operator}"