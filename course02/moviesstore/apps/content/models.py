from django.db import models


class Movie(models.Model):
    """
    电影基础信息（商城维度）
    """

    class AccessType(models.TextChoices):
        FREE = "FREE", "免费"
        BUY_ONLY = "BUY_ONLY", "仅购买"
        BUY_OR_VIP = "BUY_OR_VIP", "购买或会员"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "草稿"
        ONLINE = "ONLINE", "上架"
        OFFLINE = "OFFLINE", "下架"

    title = models.CharField(
        max_length=255,
        verbose_name="电影名称",
    )
    original_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="原片名",
    )
    release_year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="上映年份",
    )

    access_type = models.CharField(
        max_length=20,
        choices=AccessType.choices,
        verbose_name="观看方式",
    )
    price_coin = models.BigIntegerField(
        default=0,
        verbose_name="价格（金豆）",
        help_text="0 表示免费",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name="状态",
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="上架时间",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "movie"
        verbose_name = "电影"
        verbose_name_plural = "电影"

    def __str__(self):
        return self.title


class MovieDetail(models.Model):
    """
    电影详情（内容维度）
    """

    movie = models.OneToOneField(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    synopsis = models.TextField(
        verbose_name="剧情简介",
    )
    duration_minutes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="片长（分钟）",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "movie_detail"
        verbose_name = "电影详情"
        verbose_name_plural = "电影详情"


class MovieAsset(models.Model):
    """
    电影资源（封面 / 视频 / 海报）
    """

    class AssetType(models.TextChoices):
        COVER = "COVER", "封面"
        VIDEO = "VIDEO", "视频"
        POSTER = "POSTER", "海报"

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="电影",
    )
    asset_type = models.CharField(
        max_length=20,
        choices=AssetType.choices,
        verbose_name="资源类型",
    )
    asset_url = models.CharField(
        max_length=500,
        verbose_name="资源地址",
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="是否主资源",
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name="排序值",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    class Meta:
        db_table = "movie_asset"
        verbose_name = "电影资源"
        verbose_name_plural = "电影资源"
