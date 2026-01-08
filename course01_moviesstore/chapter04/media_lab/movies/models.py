from django.db import models
from django.utils import timezone


def movie_cover_path(instance, filename):
    """
    电影封面上传路径

    ❗注意：
    - upload_to 执行时，instance.created_at 还不存在（None）
    - 不能用 instance.pk（首次保存前也是 None）
    - 必须使用 timezone.now() 或 uuid

    目录示例：
    media/
      covers/
        2026-01/
          cover_xxx.jpg
    """
    dt = timezone.now()
    return f"covers/{dt:%Y-%m}/{filename}"


def movie_photo_path(instance, filename):
    """
    电影剧照上传路径（多图）

    剧照一定是在 Movie 已保存后创建：
    - instance.movie_id 一定有值
    - 但依然做兜底，防止未来代码调整

    目录示例：
    media/
      photos/
        2026-01/
          movie_12/
            photo_xxx.jpg
    """
    dt = timezone.now()
    movie_id = instance.movie_id or "temp"
    return f"photos/{dt:%Y-%m}/movie_{movie_id}/{filename}"


class Movie(models.Model):
    """
    电影模型（主表）

    - cover：单图（封面）
    - photos：反向关系 movie.photos.all()
    """

    title = models.CharField(
        "标题",
        max_length=100,
        db_index=True,
    )

    description = models.TextField(
        "简介",
        blank=True,
    )

    cover = models.ImageField(
        "封面图",
        upload_to=movie_cover_path,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        "创建时间",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "电影"
        verbose_name_plural = "电影管理"

    def __str__(self):
        return self.title


class MoviePhoto(models.Model):
    """
    电影剧照（子表，多对一）

    - movie：外键
    - image：图片文件
    """

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="所属电影",
    )

    image = models.ImageField(
        "剧照",
        upload_to=movie_photo_path,
    )

    caption = models.CharField(
        "说明",
        max_length=50,
        blank=True,
    )

    created_at = models.DateTimeField(
        "创建时间",
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "电影剧照"
        verbose_name_plural = "剧照管理"

    def __str__(self):
        return f"{self.movie.title} - photo#{self.pk}"
