from django.contrib import admin
from apps.movies.models import Genre, Movie

@admin.register(Genre)  # ✅ 推荐：紧凑、可读性强
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]


# ✅ 你也可以用 admin.site.register
class MovieAdmin(admin.ModelAdmin):
    """
    演示最常用的 Admin 配置项：
    - list_display：列表显示
    - list_filter：右侧筛选
    - search_fields：搜索
    - ordering：排序
    """
    list_display = ["id", "title", "genre", "price", "is_published", "created_at"]
    list_filter = ["genre", "is_published", "created_at"]
    search_fields = ["title", "genre__name"]
    ordering = ["-created_at"]
    list_per_page = 20

admin.site.register(Movie, MovieAdmin)  # ✅ 经典写法