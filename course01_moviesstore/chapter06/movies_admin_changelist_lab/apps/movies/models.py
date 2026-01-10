from django.conf import settings
from django.db import models

class Genre(models.Model):
    name = models.CharField("类型", max_length=50, unique=True)

    class Meta:
        verbose_name = "类型"
        verbose_name_plural = "类型"

    def __str__(self) -> str:
        return self.name


class Director(models.Model):
    name = models.CharField("导演", max_length=50, db_index=True)

    class Meta:
        verbose_name = "导演"
        verbose_name_plural = "导演"

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    STATUS_CHOICES = (
        (1, "草稿"),
        (2, "待上架"),
        (3, "已上架"),
        (4, "已下架"),
    )

    title = models.CharField("片名", max_length=120, db_index=True)
    genre = models.ForeignKey(Genre, verbose_name="类型", on_delete=models.PROTECT)
    director = models.ForeignKey(Director, verbose_name="导演", on_delete=models.PROTECT)

    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=19.90)
    score = models.DecimalField("评分", max_digits=3, decimal_places=1, default=7.5)
    status = models.IntegerField("运营状态", choices=STATUS_CHOICES, default=2)

    poster_url = models.URLField("海报URL", blank=True, default="", help_text="用于列表页图片预览（可为空）")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="创建人",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_movies_changelist",
    )
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title