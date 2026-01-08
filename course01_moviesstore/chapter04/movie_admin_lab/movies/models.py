from django.db import models

CATEGORY_CHOICES = [
    ("action", "动作"),
    ("sci", "科幻"),
    ("comedy", "喜剧"),
    ("love", "爱情"),
    ("crime", "犯罪"),
]


class Movie(models.Model):
    """
    列表页专用字段：created_at（排序核心）、price/stock（聚合示例）、rating（均值示例）
    """
    title = models.CharField("标题", max_length=100)
    category = models.CharField("分类", max_length=20, choices=CATEGORY_CHOICES, db_index=True)

    rating = models.DecimalField("评分", max_digits=3, decimal_places=1, default=0, db_index=True)
    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=0)  # Sum/Avg 示例
    stock = models.PositiveIntegerField("库存", default=0)  # Sum 示例

    is_hot = models.BooleanField("热门", default=False, db_index=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]  # ✅ 默认按最新创建

    def __str__(self):
        return self.title
