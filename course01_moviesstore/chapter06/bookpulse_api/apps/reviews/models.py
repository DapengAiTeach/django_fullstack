from django.db import models


class Review(models.Model):
    """
    Review = 资源（Resource）
    对应 RESTful endpoints：/api/reviews/
    """

    book_title = models.CharField("书名", max_length=200)
    content = models.TextField("书评内容")
    rating = models.PositiveSmallIntegerField("评分(1~5)", default=5)

    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "reviews_review"
        verbose_name = "书评"
        verbose_name_plural = "书评"

    def __str__(self) -> str:
        return f"{self.book_title}({self.rating})"