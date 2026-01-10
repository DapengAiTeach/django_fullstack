from django.db import models

class Genre(models.Model):
    name = models.CharField("类型名称", max_length=50, unique=True)

    class Meta:
        verbose_name = "电影类型"
        verbose_name_plural = "电影类型"

    def __str__(self) -> str:
        return self.name


class Director(models.Model):
    """
    导演：演示 autocomplete_fields / raw_id_fields（大数据量外键选择）
    """
    name = models.CharField("导演姓名", max_length=50, db_index=True)
    country = models.CharField("国家/地区", max_length=50, blank=True, default="")

    class Meta:
        verbose_name = "导演"
        verbose_name_plural = "导演"

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField("标签名", max_length=30, unique=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    """
    电影：用于讲透 ModelAdmin 列表页 + 表单页的全部基础配置项。
    """
    LEVEL_CHOICES = (
        (1, "A级（普通）"),
        (2, "S级（重点）"),
        (3, "SS级（王牌）"),
    )

    title = models.CharField("电影标题", max_length=120)
    genre = models.ForeignKey(Genre, verbose_name="类型", on_delete=models.PROTECT)
    director = models.ForeignKey(Director, verbose_name="导演", on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True)

    price = models.DecimalField("价格", max_digits=8, decimal_places=2, default=19.90)
    level = models.IntegerField("运营等级", choices=LEVEL_CHOICES, default=1)

    is_published = models.BooleanField("已上架", default=True)
    stock = models.IntegerField("库存", default=100)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"
        ordering = ["-created_at"]  # ✅ 默认排序（也会被 ModelAdmin.ordering 覆盖）

    def __str__(self) -> str:
        return self.title