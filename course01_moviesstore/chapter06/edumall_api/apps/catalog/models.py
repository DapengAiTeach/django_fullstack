from django.db import models


class Product(models.Model):
    title = models.CharField("标题", max_length=200)
    sku = models.CharField("SKU", max_length=64, unique=True)
    price = models.DecimalField("价格", max_digits=10, decimal_places=2)
    stock = models.IntegerField("库存", default=0)
    is_active = models.BooleanField("是否上架", default=True)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "catalog_product"
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self) -> str:
        return f"{self.title}({self.sku})"