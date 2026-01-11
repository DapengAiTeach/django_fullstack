from django.db import models


class Movie(models.Model):
    """
    Movie 是我们的核心资源（Resource）。
    RESTful 的资源名：movies
    对应 API：/api/movies/
    """

    title = models.CharField("标题", max_length=200)
    overview = models.TextField("简介", blank=True)
    release_date = models.DateField("上映日期", null=True, blank=True)
    rating = models.DecimalField("评分", max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "movies_movie"
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self) -> str:
        return self.title