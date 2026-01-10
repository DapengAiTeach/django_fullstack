from django.conf import settings
from django.db import models

class Movie(models.Model):
    RISK_CHOICES = (
        (1, "低风险"),
        (2, "中风险"),
        (3, "高风险"),
    )

    title = models.CharField("电影标题", max_length=120, db_index=True)

    price = models.DecimalField("原价", max_digits=8, decimal_places=2, default=19.90)
    discount = models.IntegerField("折扣(%)", default=0, help_text="0~90，表示打折百分比，例如 20 表示打 8 折")

    # ✅ 系统计算字段：必须防止用户在 admin 里篡改
    final_price = models.DecimalField("最终价(系统计算)", max_digits=8, decimal_places=2, default=19.90)

    is_published = models.BooleanField("已上架", default=True)

    # ✅ 只有超级用户才允许改：用于演示 get_form / 防越权
    risk_level = models.IntegerField("风控等级", choices=RISK_CHOICES, default=1)

    # ✅ 隐藏字段：用于演示“隐藏字段篡改防御”
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_movies",
    )

    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "电影商品"
        verbose_name_plural = "电影商品"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title