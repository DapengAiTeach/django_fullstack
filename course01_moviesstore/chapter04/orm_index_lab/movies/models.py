# movies/models.py
from django.db import models

class Director(models.Model):
    """
    演示点：
    - unique：导演名唯一
    - verbose_name_plural：Admin里复数名更友好
    """
    name = models.CharField("导演名", max_length=50, unique=True)

    class Meta:
        verbose_name = "导演"
        verbose_name_plural = "导演管理"  # ✅ 让后台更像“产品级”

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    演示点：
    - db_index：经常用于筛选/排序的字段加索引
    - indexes：复合索引（MySQL 8 非常关键）
    - ordering：默认排序（列表页、后台页直接受益）
    """
    title = models.CharField("标题", max_length=100, db_index=True)  # ✅ 搜索常用
    director = models.ForeignKey(Director, on_delete=models.PROTECT, related_name="movies")

    # 常见筛选字段：分类 + 上架状态 + 创建时间
    category = models.CharField("分类", max_length=20, db_index=True)
    is_active = models.BooleanField("上架", default=True, db_index=True)

    # 常见排序/范围查询字段：评分、创建时间
    rating = models.DecimalField("评分", max_digits=3, decimal_places=1, default=0, db_index=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影管理"
        ordering = ["-created_at"]  # ✅ 默认最新在前（列表页最常见）
        indexes = [
            # ✅ 复合索引：分类 + 上架（后台筛选非常频繁）
            models.Index(fields=["category", "is_active"], name="idx_movie_cat_active"),

            # ✅ 复合索引：上架 + 创建时间（上架列表按时间排序很常见）
            models.Index(fields=["is_active", "-created_at"], name="idx_movie_active_ct"),
        ]

    def __str__(self):
        return self.title


class MovieSKU(models.Model):
    """
    演示点：
    - unique_together：同一部电影 + 同一个版本 只能出现一次
      典型业务：同一商品不同规格（清晰度/语言/版本）
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="skus")
    edition = models.CharField("版本", max_length=20)  # 例如：HD / 4K / DirectorCut
    price = models.DecimalField("价格", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "电影SKU"
        verbose_name_plural = "SKU管理"
        unique_together = ("movie", "edition")  # ✅ Django层面的联合唯一约束
        indexes = [
            models.Index(fields=["movie", "edition"], name="idx_sku_movie_edition"),
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.edition}"