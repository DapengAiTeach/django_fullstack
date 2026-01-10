from django.db import models

class Movie(models.Model):
    title = models.CharField("电影名", max_length=100)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self):
        return self.title