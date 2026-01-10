from django.db import models

class Genre(models.Model):
    """
    电影类型：用于演示 Admin 的列表、筛选、搜索、外键选择等能力。
    """
    name = models.CharField("类型名称", max_length=50, unique=True)

    class Meta:
        verbose_name = "电影类型"
        verbose_name_plural = "电影类型"

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    """
    电影：用于演示 Admin 的 list_display、list_filter、search_fields 等。
    """
    title = models.CharField("电影标题", max_length=120)
    genre = models.ForeignKey(Genre, verbose_name="类型", on_delete=models.PROTECT)
    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=19.90)
    is_published = models.BooleanField("已上架", default=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title