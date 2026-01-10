from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    # 电影分类（单选）
    name = models.CharField("分类名称", max_length=50, unique=True)

    class Meta:
        verbose_name = "电影分类"
        verbose_name_plural = "电影分类"

    def __str__(self) -> str:
        return self.name


class Country(models.Model):
    # 产地（单选）
    name = models.CharField("产地名称", max_length=50, unique=True)

    class Meta:
        verbose_name = "产地"
        verbose_name_plural = "产地"

    def __str__(self) -> str:
        return self.name


class Language(models.Model):
    # 语言（单选）
    name = models.CharField("语言名称", max_length=50, unique=True)

    class Meta:
        verbose_name = "语言"
        verbose_name_plural = "语言"

    def __str__(self) -> str:
        return self.name


class Person(models.Model):
    # 演职人员（导演/编剧/演员）
    name_cn = models.CharField("中文名", max_length=100)
    name_en = models.CharField("英文名", max_length=100, blank=True)
    avatar = models.ImageField("头像", upload_to="movies/people/", blank=True, null=True)
    bio = models.TextField("简介", blank=True)

    class Meta:
        verbose_name = "演职人员"
        verbose_name_plural = "演职人员"

    def __str__(self) -> str:
        return self.name_cn


class Movie(models.Model):
    # 电影主表（电商商品化）
    title_cn = models.CharField("译名/中文名", max_length=200)
    title_original = models.CharField("片名/原名", max_length=200, blank=True)
    slug = models.SlugField("URL 标识", max_length=220, unique=True, blank=True)
    year = models.PositiveSmallIntegerField("年代")
    genre = models.ForeignKey(Genre, verbose_name="类别", on_delete=models.PROTECT)
    country = models.ForeignKey(Country, verbose_name="产地", on_delete=models.PROTECT)
    language = models.ForeignKey(Language, verbose_name="语言", on_delete=models.PROTECT)
    subtitle = models.CharField("字幕", max_length=50, blank=True)
    release_date = models.DateField("上映日期")
    publish_date = models.DateField("发布时间")
    imdb_rating = models.DecimalField("IMDb 评分", max_digits=3, decimal_places=1, blank=True, null=True)
    imdb_votes = models.PositiveIntegerField("IMDb 评分人数", blank=True, null=True)
    douban_rating = models.DecimalField("豆瓣评分", max_digits=3, decimal_places=1, blank=True, null=True)
    douban_votes = models.PositiveIntegerField("豆瓣评分人数", blank=True, null=True)
    duration_minutes = models.PositiveSmallIntegerField("片长(分钟)")
    summary = models.TextField("简介", blank=True)
    cover = models.ImageField("封面", upload_to="movies/covers/")
    price = models.DecimalField("价格", max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField("库存", default=0)
    is_on_sale = models.BooleanField("是否上架", default=True)
    is_hot = models.BooleanField("是否热门", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self) -> str:
        return self.title_cn

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_cn)[:220]
        super().save(*args, **kwargs)


class MovieCredit(models.Model):
    ROLE_DIRECTOR = "director"
    ROLE_WRITER = "writer"
    ROLE_ACTOR = "actor"
    ROLE_CHOICES = [
        (ROLE_DIRECTOR, "Director"),
        (ROLE_WRITER, "Writer"),
        (ROLE_ACTOR, "Actor"),
    ]

    # 电影与演职人员的关联表
    movie = models.ForeignKey(Movie, verbose_name="电影", on_delete=models.CASCADE, related_name="credits")
    person = models.ForeignKey(Person, verbose_name="演职人员", on_delete=models.PROTECT, related_name="credits")
    role = models.CharField("角色类型", max_length=20, choices=ROLE_CHOICES)
    sort = models.PositiveSmallIntegerField("排序", default=0)

    class Meta:
        ordering = ["role", "sort", "id"]
        verbose_name = "电影演职人员"
        verbose_name_plural = "电影演职人员"

    def __str__(self) -> str:
        return f"{self.movie.title_cn} - {self.person.name_cn} ({self.role})"
