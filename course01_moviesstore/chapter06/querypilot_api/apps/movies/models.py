from django.db import models


class Movie(models.Model):
    class Genre(models.TextChoices):
        ACTION = "ACTION", "Action"
        DRAMA = "DRAMA", "Drama"
        COMEDY = "COMEDY", "Comedy"
        SCI_FI = "SCI_FI", "Sci-Fi"

    title = models.CharField("标题", max_length=120)
    genre = models.CharField("类型", max_length=20, choices=Genre.choices)
    year = models.PositiveIntegerField("年份")
    rating = models.DecimalField("评分", max_digits=3, decimal_places=1)
    is_hot = models.BooleanField("热门", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        db_table = "movies_movie"
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self) -> str:
        return f"{self.title}({self.year})"