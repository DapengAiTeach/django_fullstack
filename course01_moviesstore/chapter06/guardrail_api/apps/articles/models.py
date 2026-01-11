from django.db import models
from django.conf import settings


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField("标题", max_length=120)
    content = models.TextField("内容")

    is_published = models.BooleanField("是否发布", default=False)
    is_locked = models.BooleanField("是否锁定", default=False)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "articles_article"
        verbose_name = "文章"
        verbose_name_plural = "文章"

        # DjangoModelPermissions 需要这些默认权限
        permissions = [
            ("publish_article", "Can publish article"),
            ("lock_article", "Can lock article"),
        ]

    def __str__(self) -> str:
        return f"{self.title}({self.author_id})"