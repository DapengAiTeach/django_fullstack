from django.db import models
from django.conf import settings
from apps.content.models import Movie


class PurchaseOrder(models.Model):
    """
    购买订单主表
    """

    class Status(models.TextChoices):
        CREATED = "CREATED", "已创建"
        COMPLETED = "COMPLETED", "已完成"
        CANCELLED = "CANCELLED", "已取消"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="用户",
    )
    total_coin = models.BigIntegerField(
        verbose_name="订单总金币",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="订单状态",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "purchase_order"
        verbose_name = "购买订单"
        verbose_name_plural = "购买订单"

    def __str__(self) -> str:
        return f"订单#{self.id} - {self.user}"


class PurchaseOrderItem(models.Model):
    """
    订单项（对应具体电影）
    """

    order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        verbose_name="订单",
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    price_coin = models.BigIntegerField(
        verbose_name="购买价格（金豆）",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "purchase_order_item"
        verbose_name = "订单项"
        verbose_name_plural = "订单项"

    def __str__(self) -> str:
        return f"订单#{self.order_id} - {self.movie}"


class PurchaseLicense(models.Model):
    """
    购买授权表
    - 一个用户对一部电影只有一条授权记录
    - 权限判断以此表为准，不以订单为准
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
    order_item = models.OneToOneField(
        PurchaseOrderItem,
        on_delete=models.CASCADE,
        verbose_name="订单项",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="授权时间",
    )

    class Meta:
        db_table = "purchase_license"
        verbose_name = "购买授权"
        verbose_name_plural = "购买授权"
        unique_together = ("user", "movie")

    def __str__(self) -> str:
        return f"{self.user} - {self.movie}"
