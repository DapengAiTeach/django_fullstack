from django.contrib import admin

from .models import Country, Genre, Language, Movie, MovieCredit, Person


# ===== 维度表（分类/产地/语言）=====


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    # 分类名称可快速检索与排序，便于后台批量维护
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    # 产地表用于单选，保持列表简洁
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    # 语言表用于单选，保持列表简洁
    search_fields = ["name"]
    ordering = ["name"]


# ===== 演职人员 =====


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    # 支持中英文检索，便于快速定位人员
    list_display = ["name_cn", "name_en"]
    search_fields = ["name_cn", "name_en"]
    ordering = ["name_cn"]


# ===== 电影与演职人员关联（Inline）=====


class MovieCreditInline(admin.TabularInline):
    # 通过内联方式在电影页直接维护导演/编剧/演员
    model = MovieCredit
    extra = 1
    autocomplete_fields = ["person"]
    fields = ["person", "role", "sort"]


# ===== 电影主表（商城商品）=====


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # 列表页展示关键信息，便于电商运营与内容维护
    list_display = [
        "title_cn",
        "year",
        "genre",
        "country",
        "language",
        "price",
        "stock",
        "is_on_sale",
        "is_hot",
    ]
    list_filter = ["genre", "country", "language", "is_on_sale", "is_hot", "year"]
    search_fields = ["title_cn", "title_original", "summary"]
    ordering = ["-publish_date", "-id"]
    list_editable = ["price", "stock", "is_on_sale", "is_hot"]

    # 自动生成 URL 标识，方便后续前台路由
    prepopulated_fields = {"slug": ("title_cn",)}

    # 电影的演职人员维护采用内联方式
    inlines = [MovieCreditInline]

    # 外键使用自动补全，提升后台录入效率
    autocomplete_fields = ["genre", "country", "language"]

    # 创建/更新时间只读，避免误修改
    readonly_fields = ["created_at", "updated_at"]

    # 表单分区，降低复杂表单的阅读成本
    fieldsets = (
        (
            "基础信息",
            {
                "fields": (
                    "title_cn",
                    "title_original",
                    "slug",
                    "cover",
                    "summary",
                )
            },
        ),
        (
            "发行与评分",
            {
                "fields": (
                    "year",
                    "release_date",
                    "publish_date",
                    "duration_minutes",
                    "imdb_rating",
                    "imdb_votes",
                    "douban_rating",
                    "douban_votes",
                )
            },
        ),
        (
            "分类与语言",
            {"fields": ("genre", "country", "language", "subtitle")},
        ),
        (
            "商城属性",
            {"fields": ("price", "stock", "is_on_sale", "is_hot")},
        ),
        (
            "系统信息",
            {"fields": ("created_at", "updated_at")},
        ),
    )
