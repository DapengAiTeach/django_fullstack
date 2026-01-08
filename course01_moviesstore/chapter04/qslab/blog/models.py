from django.db import models


class Tag(models.Model):
    """
    标签：用于演示 distinct / values_list 的典型场景
    """
    name = models.CharField(max_length=32, unique=True, verbose_name="标签名")

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    文章：用于演示 QuerySet 惰性执行、链式调用、count/exists 等
    """
    title = models.CharField(max_length=120, verbose_name="标题")
    views = models.IntegerField(default=0, verbose_name="浏览量")
    is_published = models.BooleanField(default=True, verbose_name="是否发布")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    # 多对多：一篇文章可多个标签
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="articles",
        verbose_name="标签",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title
