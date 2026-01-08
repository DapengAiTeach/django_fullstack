# shop/models.py
from django.db import models

class Product(models.Model):
    """
    商品（电影票/会员/影片周边都行）
    stock：库存（并发写最容易出事故的字段）
    """
    name = models.CharField("商品名", max_length=80, unique=True)
    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=0)
    stock = models.PositiveIntegerField("库存", default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "已创建(待支付)"
        PAID = "PAID", "已支付"
        CANCELED = "CANCELED", "已取消(回滚库存)"

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 演示“支付回调幂等”：第三方支付单号（可为空）
    payment_no = models.CharField("支付单号", max_length=64, blank=True, default="")

    def __str__(self):
        return f"Order#{self.id}({self.status})"


class OrderItem(models.Model):
    """
    订单项：一个订单对应一个商品（为了教学简化）
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="item")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)
    deal_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"