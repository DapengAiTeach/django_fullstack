from decimal import Decimal
from django.db import models

class Movie(models.Model):
    """
    电影商品：用于下单时选择商品（OrderItem 外键指向 Movie）
    """
    title = models.CharField("电影标题", max_length=120, db_index=True)
    price = models.DecimalField("售价", max_digits=8, decimal_places=2, default=19.90)
    is_published = models.BooleanField("已上架", default=True)

    class Meta:
        verbose_name = "电影商品"
        verbose_name_plural = "电影商品"

    def __str__(self) -> str:
        return self.title


class Order(models.Model):
    """
    订单主表：演示 Inline 主表
    """
    STATUS_CHOICES = (
        (1, "待支付"),
        (2, "已支付"),
        (3, "已取消"),
    )

    order_no = models.CharField("订单号", max_length=32, unique=True, db_index=True)
    customer_name = models.CharField("客户名", max_length=50)
    status = models.IntegerField("订单状态", choices=STATUS_CHOICES, default=1)

    total_amount = models.DecimalField("订单总额(系统计算)", max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.order_no


class OrderItem(models.Model):
    """
    订单明细：演示 Inline 子表
    """
    order = models.ForeignKey(Order, verbose_name="所属订单", on_delete=models.CASCADE, related_name="items")
    movie = models.ForeignKey(Movie, verbose_name="电影", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("数量", default=1)
    unit_price = models.DecimalField("成交单价", max_digits=8, decimal_places=2, default=Decimal("0.00"))
    line_total = models.DecimalField("小计(系统计算)", max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name = "订单明细"
        verbose_name_plural = "订单明细"

    def __str__(self) -> str:
        return f"{self.order.order_no} - {self.movie.title}"