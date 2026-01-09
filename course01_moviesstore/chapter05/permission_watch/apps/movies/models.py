from django.db import models

class Movie(models.Model):
    """
    ✅ 默认权限自动生成机制：
    - 当你执行 makemigrations + migrate 后
    - Django 会在迁移过程中为每个模型生成 4 条默认权限：
      add_movie / change_movie / delete_movie / view_movie
    - 并写入数据库的 auth_permission 表

    ✅ 注意：默认权限不是写在代码里判断的 if，而是“数据库里的记录”。
    """
    title = models.CharField("片名", max_length=100)
    year = models.PositiveIntegerField("年份", default=2020)

    def __str__(self):
        return f"{self.title} ({self.year})"