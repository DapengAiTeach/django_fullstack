from django.conf import settings
from django.db import models

class Director(models.Model):
    """
    一对多：导演 -> 电影
    一个导演可以拍多部电影
    """
    name = models.CharField("导演名", max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    电影：属于某个导演（ForeignKey）
    """
    title = models.CharField("标题", max_length=100)
    director = models.ForeignKey(
        Director,
        on_delete=models.PROTECT,  # ⭐ 必考点：保护策略（不允许删掉还有电影的导演）
        related_name="movies",
    )

    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    """
    订单：属于某个用户（用户 -> 订单 是一对多）
    订单与电影是多对多，但我们要“带额外字段”，所以必须用中间表！
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ManyToManyField 指向 Movie，但通过中间表 OrderItem
    movies = models.ManyToManyField(
        Movie,
        through="OrderItem",
        related_name="orders",
    )

    def __str__(self):
        return f"Order#{self.id} by {self.user.username}"


class OrderItem(models.Model):
    """
    ⭐ 带额外字段的中间表（多对多进阶必会）
    - 一个订单里可以有多部电影
    - 一部电影也可能出现在多个订单里
    - 每一行 OrderItem 代表：订单中的一个商品项
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField("数量", default=1)
    deal_price = models.DecimalField("成交价", max_digits=8, decimal_places=2)

    class Meta:
        unique_together = ("order", "movie")  # 同一订单同一电影只出现一次

    def __str__(self):
        return f"{self.order_id} - {self.movie.title} x{self.quantity}"