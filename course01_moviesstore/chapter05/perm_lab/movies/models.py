from django.db import models


class Movie(models.Model):
    """
    ✅ 只要有模型，Django 就会为它自动生成默认权限：
    - add_movie
    - change_movie
    - delete_movie
    - view_movie

    这些权限最终会进入 auth_permission 表（Permission 的数据库表）。
    """
    title = models.CharField("片名", max_length=100)
    year = models.PositiveIntegerField("年份", default=2020)

    class Meta:
        # ✅ 自定义业务权限（演示 Permission 的“本质”）
        permissions = [
            ("publish_movie", "可以发布电影"),
            ("export_movie", "可以导出电影"),
        ]

    def __str__(self):
        return f"{self.title} ({self.year})"
