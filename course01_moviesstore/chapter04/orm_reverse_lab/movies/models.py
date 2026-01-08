# movies/models.py
from django.db import models


class Director(models.Model):
    name = models.CharField("导演名", max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField("标题", max_length=100)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    # ✅ 一对多：导演 -> 电影
    # related_name="movies"：导演对象可以用 director.movies 反向拿到电影集合（最推荐）
    director = models.ForeignKey(
        Director,
        on_delete=models.PROTECT,
        related_name="movies",
    )

    def __str__(self):
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        # 故意不写 related_name，让学生看到“默认反向名从哪来”
        # 默认反向访问：movie.review_set
    )

    nickname = models.CharField("昵称", max_length=30)
    content = models.CharField("评论内容", max_length=200)
    score = models.PositiveSmallIntegerField("评分", default=5)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return f"{self.nickname}({self.score})"
