# movies/admin.py
from django.contrib import admin
from .models import Director, Movie, Review


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "created_at")
    list_filter = ("director",)
    search_fields = ("title",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "nickname", "score", "created_at")
    list_filter = ("score",)
    search_fields = ("nickname", "content", "movie__title")  # ✅ 正向/反向切换：跨表查
