from django.db import models
from apps.catalog.models import Product


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField("评分(1~5)")
    content = models.TextField("评价内容")

    # 展示作者名：为了演示 write_only -> 存储字段的映射
    author_display = models.CharField("作者展示名", max_length=80, default="匿名用户")

    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "reviews_review"
        verbose_name = "评价"
        verbose_name_plural = "评价"

    def __str__(self) -> str:
        return f"{self.product_id}:{self.rating}"