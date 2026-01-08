# movies/models.py
from django.db import models

class Director(models.Model):
    name = models.CharField("导演名", max_length=50, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("标签", max_length=20, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField("标题", max_length=100)
    director = models.ForeignKey(
        Director,
        on_delete=models.PROTECT,
        related_name="movies",
    )
    tags = models.ManyToManyField(Tag, related_name="movies", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    nickname = models.CharField("昵称", max_length=30)
    score = models.PositiveSmallIntegerField("评分", default=8)
    content = models.CharField("内容", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname}({self.score})"