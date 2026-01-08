# movies/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    title = models.CharField("片名", max_length=100)
    year = models.PositiveIntegerField("年份", default=2020)
    summary = models.TextField("简介", blank=True)

    # ✅ 对象归属：用于演示“同样有权限，但只能改自己的”
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies", verbose_name="创建者")

    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        # ✅ 自定义业务权限：不仅 add/change/delete/view
        permissions = [
            ("publish_movie", "可以发布电影"),
            ("export_movie", "可以导出电影"),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"