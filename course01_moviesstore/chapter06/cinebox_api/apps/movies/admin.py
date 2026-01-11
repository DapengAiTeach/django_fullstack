from django.contrib import admin
from apps.movies.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    让学生看到：同一份数据模型（Movie）
    - Admin 用来“运营/管理”
    - DRF API 用来“对外服务”
    """
    list_display = ("id", "title", "release_date", "rating", "created_at")
    search_fields = ("title",)
    list_filter = ("release_date",)
    ordering = ("-created_at",)