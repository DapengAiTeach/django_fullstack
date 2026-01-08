# movies/models.py
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
    影片模型：专门为“条件组合查询”准备字段
    """
    title = models.CharField("标题", max_length=100)
    summary = models.TextField("简介", blank=True)

    category = models.CharField(
        "分类",
        max_length=20,
        choices=CATEGORY_CHOICES,
        db_index=True,  # ✅ 常被筛选的字段，建议加索引
    )

    rating = models.DecimalField(
        "评分",
        max_digits=3,
        decimal_places=1,
        default=0.0,
        db_index=True,
    )
    is_hot = models.BooleanField(
        "热门",
        default=False,
        db_index=True,
    )

    created_at = models.DateTimeField(
        "创建时间",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
